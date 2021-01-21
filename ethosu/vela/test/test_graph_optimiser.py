# Copyright (C) 2020 Arm Limited or its affiliates. All rights reserved.
#
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Description:
# Unit tests for graph_optimiser
import numpy as np

from ethosu.vela.data_type import DataType
from ethosu.vela.graph_optimiser import convert_batched_fc_shape
from ethosu.vela.graph_optimiser import optimise_graph_a
from ethosu.vela.graph_optimiser import optimise_pad
from ethosu.vela.nn_graph import Graph
from ethosu.vela.operation import Op
from ethosu.vela.operation import Padding
from ethosu.vela.rewrite_graph import verify_graph_health
from ethosu.vela.tensor import create_const_tensor
from ethosu.vela.tensor import Shape4D
from ethosu.vela.tensor import Tensor
from ethosu.vela.test import testutil


def test_convert_batched_fc():
    """Tests shape conversion of batched fully connected"""
    ifm_shape = [4, 8]
    ifm = create_const_tensor("test_in", ifm_shape, np.uint8, np.zeros(ifm_shape))
    w_shape = [8, 4]
    weights = create_const_tensor("weight_in", w_shape, np.uint8, np.zeros(w_shape))
    ofm = Tensor(ifm.shape, np.uint8, "test_out")
    op = testutil.create_op(Op.FullyConnected, [ifm, weights], ofm)

    ifm.consumer_list.append(op)

    prev_op = op.clone()
    prev_op.ifm_shapes = op.ifm_shapes.copy()
    prev_op.ofm_shapes = op.ofm_shapes.copy()

    conv_op = convert_batched_fc_shape(op, None, None)

    assert conv_op.ifm == prev_op.ifm
    assert conv_op.ofm == prev_op.ofm
    assert op.ifm_shapes[0] == Shape4D([1, 2, 2, 8])
    assert op.ofm_shapes[0] == Shape4D([1, 2, 2, 8])
    assert conv_op.type == Op.FullyConnected
    assert len(conv_op.ifm.shape) == 2
    assert len(conv_op.ofm.shape) == 2
    assert conv_op.ifm.shape == conv_op.ofm.shape

    ifm.shape = [1, 8]
    weights.shape = [8, 1]
    ofm.shape = [1, 8]
    op = testutil.create_op(Op.FullyConnected, [ifm, weights], ofm)
    ifm.consumer_list.append(op)

    prev_op = op.clone()
    prev_op.ifm_shapes = op.ifm_shapes.copy()
    prev_op.ofm_shapes = op.ofm_shapes.copy()

    conv_op = convert_batched_fc_shape(op, None, None)

    assert conv_op.ifm == prev_op.ifm
    assert conv_op.ofm == prev_op.ofm
    assert op.ifm_shapes[0] == prev_op.ifm_shapes[0]
    assert op.ofm_shapes[0] == prev_op.ofm_shapes[0]
    assert conv_op.type == Op.FullyConnected
    assert len(conv_op.ifm.shape) == 2
    assert len(conv_op.ofm.shape) == 2
    assert conv_op.ifm.shape == conv_op.ofm.shape


def test_optimise_pad():
    """
    Tests that the PAD operator is bypassed when followed by a convolution operator,
    and that the padding of the convolution operation is correctly updated
    """
    # Create Pad operation followed by Conv2D
    quant = testutil.default_quant_params()
    in_tens = Tensor([1, 76, 75, 64], DataType.uint8, "input")
    in_tens.quantization = quant
    pad_input = create_const_tensor("pad_input", [4, 2], DataType.int32, [[0, 0], [2, 1], [1, 1], [0, 0]])
    temp_tens = Tensor([1, 79, 77, 64], DataType.uint8, "pad_out")
    temp_tens.quantization = quant.clone()
    out_tens = Tensor([1, 76, 75, 64], DataType.uint8, "output")
    out_tens.quantization = quant.clone()
    weight_tens = Tensor([5, 3, 64, 64], DataType.uint8, "weights")
    weight_tens.values = np.zeros(weight_tens.shape)
    weight_tens.quant_values = np.zeros(weight_tens.shape, np.uint8)
    weight_tens.quantization = quant.clone()

    bias_tens = Tensor([64], DataType.int32, "biases")
    pad_op = testutil.create_op(Op.Pad, [in_tens, pad_input], temp_tens)
    attrs = {"padding": Padding.VALID, "stride_w": 2, "stride_h": 2, "dilation_w_factor": 1, "dilation_h_factor": 1}
    attrs["strides"] = (1, attrs["stride_h"], attrs["stride_w"], 1)
    pad_op.run_on_npu = True
    conv2d_op = testutil.create_op(Op.Conv2D, [temp_tens, weight_tens, bias_tens], out_tens, attrs)
    conv2d_op.run_on_npu = True
    nng = Graph()
    sg = testutil.create_subgraph([pad_op, conv2d_op])
    nng.subgraphs.append(sg)
    arch = testutil.create_arch()

    optimise_pad(conv2d_op, nng, arch)

    op = sg.output_tensors[0].ops[0]
    assert op.type == Op.Conv2D
    assert op.attrs["padding"] == Padding.EXPLICIT
    assert op.attrs["explicit_padding"] == (2, 1, 1, 1)
    assert op.ifm.shape == [1, 76, 75, 64]
    assert pad_op not in op.ifm.ops


def test_remove_reshape():
    """
    Tests that the expected reshape are removed in graph_optimisation
    """

    def setup_network():
        quant = testutil.default_quant_params()
        # create reshape1 op
        ifm_shape = [64, 16]
        reshape1_ofm_shape = [1, 4, 16, 16]
        reshape1_ifm = create_const_tensor("reshape1_in", ifm_shape, DataType.uint8, np.zeros(ifm_shape))
        reshape1_ifm.quantization = quant
        reshape1_ofm = create_const_tensor(
            "reshape1_out", reshape1_ofm_shape, DataType.uint8, np.zeros(reshape1_ofm_shape)
        )
        reshape1_ofm.quantization = quant
        shape_tens = create_const_tensor("reshape1_shape", [1], DataType.int32, reshape1_ofm_shape)
        reshape1_op = testutil.create_op(Op.Reshape, [reshape1_ifm, shape_tens], reshape1_ofm, set_ifm_ofm_shapes=False)
        reshape1_op.attrs["new_shape"] = reshape1_ofm_shape
        reshape1_op.run_on_npu = True

        # create reshape2 op
        reshape2_ofm_shape = [1, 8, 8, 16]
        reshape2_ofm = create_const_tensor(
            "reshape2_out", reshape2_ofm_shape, DataType.uint8, np.zeros(reshape2_ofm_shape)
        )
        reshape2_ofm.quantization = quant
        shape_tens = create_const_tensor("reshape2_shape", [1], DataType.int32, reshape2_ofm_shape)
        reshape2_op = testutil.create_op(Op.Reshape, [reshape1_ofm, shape_tens], reshape2_ofm, set_ifm_ofm_shapes=False)
        reshape2_op.attrs["new_shape"] = reshape2_ofm_shape
        reshape2_op.run_on_npu = True

        # create conv op
        conv_ofm = Tensor([1, 8, 8, 16], DataType.uint8, "output")
        conv_ofm.quantization = quant.clone()
        weight_tens = Tensor([1, 1, 16, 16], DataType.uint8, "weights")
        weight_tens.values = np.zeros(weight_tens.shape)
        weight_tens.quant_values = np.zeros(weight_tens.shape, np.uint8)
        weight_tens.quantization = quant.clone()
        bias_tens = Tensor([16], DataType.int32, "biases")

        attrs = {"padding": Padding.SAME, "stride_w": 1, "stride_h": 1, "dilation_w_factor": 1, "dilation_h_factor": 1}
        attrs["strides"] = (1, attrs["stride_h"], attrs["stride_w"], 1)

        conv2d_op = testutil.create_op(
            Op.Conv2D, [reshape1_ofm, weight_tens, bias_tens], conv_ofm, attrs=attrs, set_ifm_ofm_shapes=False
        )
        conv2d_op.run_on_npu = True

        # create reshape3 op
        ofm_shape = [8, 8, 16]
        reshape3_ofm = create_const_tensor("reshape3_out", ofm_shape, DataType.uint8, np.zeros(ofm_shape))
        reshape3_ofm.quantization = quant
        shape_tens = create_const_tensor("reshape3_shape", [1], DataType.int32, ofm_shape)
        reshape3_op = testutil.create_op(Op.Reshape, [conv_ofm, shape_tens], reshape3_ofm, set_ifm_ofm_shapes=False)
        reshape3_op.attrs["new_shape"] = ofm_shape
        reshape3_op.run_on_npu = True
        nng = Graph()
        sg = testutil.create_subgraph([reshape1_op, reshape2_op, conv2d_op, reshape3_op])
        nng.subgraphs.append(sg)

        return nng, reshape1_op, reshape2_op, conv2d_op, reshape3_op

    # Test1 no Reshape op is expected to remain in the NPU subgrapgh
    # but first one will be put on CPU
    # Network is Reshape-Reshape-Conv-Reshape
    # Result is cpu_Reshape-Conv
    nng, reshape1_op, reshape2_op, conv2d_op, reshape3_op = setup_network()
    arch = testutil.create_arch()
    assert verify_graph_health(nng)
    nng = optimise_graph_a(nng, arch)
    assert verify_graph_health(nng)
    assert conv2d_op.ifm == reshape1_op.ofm
    assert conv2d_op.ofm == reshape3_op.ofm

    # Test2 reshape2 with different quantisation, this Reshape op is expected to remain
    # Network is Reshape-Reshape-Conv-Reshape
    # expected is cpu_Reshape-Reshape-Conv
    nng, reshape1_op, reshape2_op, conv2d_op, reshape3_op = setup_network()
    quant_zp32 = testutil.default_quant_params()
    quant_zp32.zero_point = 32
    reshape2_op.ofm.quantization = quant_zp32
    assert verify_graph_health(nng)
    nng = optimise_graph_a(nng, arch)
    assert verify_graph_health(nng)
    assert conv2d_op.ofm == reshape3_op.ofm
