# Copyright (C) 2021 Arm Limited or its affiliates. All rights reserved.
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
# Description:
# Functions used to read from a TOSA format file.
import os.path
import struct
import sys

import numpy as np

from .nn_graph import Graph
from .nn_graph import Subgraph
from .operation import Op
from .operation import Operation
from .reader_util import align_tensor_indices_to_nng
from .reader_util import clone_and_reshape_tensor
from .reader_util import decode_str
from .reader_util import fixup_tensors
from .tensor import QuantizationParameters
from .tensor import Tensor
from .tflite_mapping import DataType
from .tosa.TosaGraph import TosaGraph as TG
from .tosa_mapping import datatype_map
from .tosa_mapping import tosa_operator_map
from .tosa_mapping import unsupported_tosa_operators


class TosaSubgraph:
    def __init__(self, file_path, graph, block):
        self.graph = graph
        self.name = decode_str(block.Name())

        self.tensors = []
        for idx in range(block.TensorsLength()):
            self.tensors.append(self.parse_tensor(block.Tensors(idx), file_path))

        for idx in range(block.OperatorsLength()):
            self.parse_operator(idx, block.Operators(idx))

        # Get the subgraph inputs and outputs
        self.inputs = self.get_sg_inputs_remove_duplicates(block)
        self.outputs = self.get_sg_outputs_remove_duplicates(block)
        fixup_tensors(self.inputs, self.tensors)

    def get_sg_inputs_remove_duplicates(self, block):
        inputs = []
        for idx in range(block.InputsLength()):
            tens_data = block.Inputs(idx)
            self.add_not_duplicate(tens_data, inputs, "input")
        return inputs

    def get_sg_outputs_remove_duplicates(self, block):
        outputs = []
        for idx in range(block.OutputsLength()):
            tens_data = block.Outputs(idx)
            self.add_not_duplicate(tens_data, outputs, "output")
        return outputs

    def add_not_duplicate(self, tens_data, tensors, warning_str):
        name = decode_str(tens_data)
        tensor = self.get_tensor_by_name(name)
        if tensor not in tensors:
            tensors.append(tensor)
        else:
            print(f"Warning: Subgraph {warning_str} tensor ({tensor}) already seen. Removing the duplicate.")

    def get_tensor_by_name(self, name):
        for tens in self.tensors:
            if tens.name == name:
                return tens
        return None

    def parse_operator(self, op_index, op_data):
        op_code = op_data.Op()
        if op_code in unsupported_tosa_operators:
            print("Unsupported Operator", op_code)
            assert False

        op_type, attr_serializer, quant_serializer, indices = tosa_operator_map[op_code]
        inputs = []
        outputs = []
        for idx in range(op_data.InputsLength()):
            input_tens = self.get_tensor_by_name(decode_str(op_data.Inputs(idx)))
            inputs.append(input_tens)
            assert input_tens is not None

        for idx in range(op_data.OutputsLength()):
            output_tens = self.get_tensor_by_name(decode_str(op_data.Outputs(idx)))
            outputs.append(output_tens)
            assert output_tens is not None

        name = "unknown_op_name"
        if len(outputs):
            name = outputs[0].name
        inputs = align_tensor_indices_to_nng(op_type, indices, inputs)
        op = Operation(op_type, name)
        op.op_index = op_index
        op.inputs = inputs
        op.outputs = outputs

        for out in op.outputs:
            out.ops = [op]

        # TODO Transpose_conv and conv3d
        if op.type.is_depthwise_conv2d_op() or op.type.is_conv2d_op() or op.type == Op.FullyConnected:
            if inputs[1].values is not None:
                if op.type == Op.FullyConnected:
                    inputs[1] = clone_and_reshape_tensor(inputs[1], (1, 0), False)
                elif op.type.is_conv2d_op():
                    inputs[1] = clone_and_reshape_tensor(inputs[1], (1, 2, 3, 0), False)
                elif op.type.is_depthwise_conv2d_op():
                    inputs[1] = clone_and_reshape_tensor(inputs[1], (1, 2, 0, 3), False)
            if op.type.needs_bias() and len(inputs) <= op_type.info.indices.biases[0]:
                # No Bias tensor
                inputs.append(None)
            if inputs[-1] and inputs[-1].values is not None:
                # Since bias tensor is used for both bias and scale,
                # a clone with a unique equivalence_id is needed
                inputs[-1] = clone_and_reshape_tensor(inputs[-1], (0,), True)

        if attr_serializer is not None:
            op.attrs = attr_serializer.deserialize(op_data)

            if "dilation" in op.attrs:
                dilation = op.attrs["dilation"]
                if len(dilation) == 2:
                    op.attrs["dilation"] = (1, dilation[0], dilation[1], 1)
                elif len(dilation) == 3:
                    # TODO CONV3D more to be done....
                    op.attrs["dilation"] = (dilation[0], dilation[1], dilation[2], 1)
            if "kernel" in op.attrs:
                kernel = op.attrs["kernel"]
                if len(kernel) == 2:
                    op.attrs["ksize"] = (1, kernel[0], kernel[1], 1)
                else:
                    # TODO CONV3D more to be done....
                    print("Unsupported kernel dimensions: ", len(kernel))
                    assert False

        if quant_serializer is not None:
            quant_info = quant_serializer.deserialize(op_data)

            # TODO tensor zero points currently set here
            # zero points part of Rescale operation, handled in tosa_graph_optimizer
            if "input_zp" in quant_info:
                self.set_tensor_zp(op.ifm, quant_info["input_zp"])
            if "weight_zp" in quant_info:
                self.set_tensor_zp(op.weights, quant_info["weight_zp"])
            if "ouput_zp" in quant_info:
                self.set_tensor_zp(op.ofm, quant_info["output_zp"])
            if "a_zp" in quant_info:
                self.set_tensor_zp(op.ifm, quant_info["a_zp"])
            if "b_zp" in quant_info:
                self.set_tensor_zp(op.ifm2, quant_info["b_zp"])

    def parse_tensor(self, tens_data, file_path):
        name = decode_str(tens_data.Name())
        np_shape = tens_data.ShapeAsNumpy()
        shape = list(np_shape) if type(np_shape) is np.ndarray else []
        tens_dtype = tens_data.Type()
        dtype = datatype_map[tens_dtype]

        tens = Tensor(shape, dtype, name)

        # Initialize quantization parameters
        tens.quantization = QuantizationParameters()

        tens.quantization.scale_f32 = 1.0
        if dtype == DataType.uint8:
            tens.quantization.quant_min = 0
            tens.quantization.quant_max = (1 << dtype.bits) - 1
        elif dtype in (DataType.int8, DataType.int16, DataType.int32, DataType.int64):
            tens.quantization.quant_min = -(1 << (dtype.bits - 1))
            tens.quantization.quant_max = (1 << (dtype.bits - 1)) - 1

        tens.values = None
        if tens_data.NpyFilename() is not None:
            try:
                fname = decode_str(tens_data.NpyFilename())
                tens.values = np.load(os.path.join(file_path, fname))
                assert list(tens.values.shape) == tens.shape
            except (struct.error, TypeError, RuntimeError) as e:
                print(f'Error: Invalid npy file. Got "{e}" ')
                sys.exit(1)

        return tens

    def set_tensor_zp(self, tens, zp):
        if tens.quantization.zero_point is None:
            tens.quantization.zero_point = zp
        elif tens.quantization.zero_point != zp:
            print(f"Error: Setting tensor zp not possible, tensor already has different zero point")
            assert False


class TosaGraph:
    def __init__(self, filename, batch_size, feed_dict, output_node_names, initialisation_nodes):

        self.op_times = {}
        if batch_size is None:
            batch_size = 1
        self.batch_size = batch_size
        self.name = os.path.splitext(os.path.basename(filename))[0]
        self.initialisation_nodes = initialisation_nodes

        with open(filename, "rb") as f:
            buf = bytearray(f.read())

        try:
            parsing_step = "parsing root"
            tosa_graph = TG.GetRootAsTosaGraph(buf, 0)

            parsing_step = "parsing version"
            self.check_version(tosa_graph)

            parsing_step = "parsing blocks length"
            file_path = os.path.dirname(filename)
            self.subgraphs = []
            for b_idx in range(tosa_graph.BlocksLength()):
                parsing_step = f"parsing block {b_idx}"
                self.subgraphs.append(TosaSubgraph(file_path, self, tosa_graph.Blocks(b_idx)))

            self.nng = Graph(self.name, self.batch_size)
            for tosa_sg in self.subgraphs:
                sg = Subgraph(tosa_sg.name)
                sg.original_inputs = tosa_sg.inputs  # Preserve the original input order
                sg.output_tensors = tosa_sg.outputs
                self.nng.subgraphs.append(sg)

        except (struct.error, TypeError, RuntimeError) as e:
            print(f'Error: Invalid .tosa file. Got "{e}" while {parsing_step}.')
            sys.exit(1)

    def check_version(self, tosa_graph):
        version = tosa_graph.Version()
        version_str = f"{version._major()}.{version._minor()}.{version._patch()}"
        if version_str != "0.22.0":
            print(f"Unsupported TOSA version: {version_str}")
            assert False


def read_tosa(filename, batch_size, feed_dict, output_node_names, initialisation_nodes):
    tosa_graph = TosaGraph(filename, batch_size, feed_dict, output_node_names, initialisation_nodes)
    nng = tosa_graph.nng
    nng.refresh_after_modification()
    return nng