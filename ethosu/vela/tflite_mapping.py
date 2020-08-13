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
# Description:
# TensorFlow Lite mapping functions used by both reader and writer.
# Contains a mapping from the various TensorFlow Lite enums and options structs, generated by the FlatBuffer code
# generator, to Vela's internal format.
import struct

import numpy as np

from .data_type import DataType
from .tflite import AbsOptions
from .tflite import AddNOptions
from .tflite import AddOptions
from .tflite import ArgMaxOptions
from .tflite import ArgMinOptions
from .tflite import BatchToSpaceNDOptions
from .tflite import BidirectionalSequenceLSTMOptions
from .tflite import BidirectionalSequenceRNNOptions
from .tflite import CallOptions
from .tflite import CastOptions
from .tflite import ConcatEmbeddingsOptions
from .tflite import ConcatenationOptions
from .tflite import Conv2DOptions
from .tflite import CosOptions
from .tflite import DensifyOptions
from .tflite import DepthToSpaceOptions
from .tflite import DepthwiseConv2DOptions
from .tflite import DequantizeOptions
from .tflite import DivOptions
from .tflite import EmbeddingLookupSparseOptions
from .tflite import EqualOptions
from .tflite import ExpandDimsOptions
from .tflite import ExpOptions
from .tflite import FakeQuantOptions
from .tflite import FillOptions
from .tflite import FloorDivOptions
from .tflite import FloorModOptions
from .tflite import FullyConnectedOptions
from .tflite import GatherNdOptions
from .tflite import GatherOptions
from .tflite import GreaterEqualOptions
from .tflite import GreaterOptions
from .tflite import HardSwishOptions
from .tflite import IfOptions
from .tflite import L2NormOptions
from .tflite import LeakyReluOptions
from .tflite import LessEqualOptions
from .tflite import LessOptions
from .tflite import LocalResponseNormalizationOptions
from .tflite import LogicalAndOptions
from .tflite import LogicalNotOptions
from .tflite import LogicalOrOptions
from .tflite import LogSoftmaxOptions
from .tflite import LSHProjectionOptions
from .tflite import LSTMOptions
from .tflite import MatrixDiagOptions
from .tflite import MatrixSetDiagOptions
from .tflite import MaximumMinimumOptions
from .tflite import MirrorPadOptions
from .tflite import MulOptions
from .tflite import NegOptions
from .tflite import NonMaxSuppressionV4Options
from .tflite import NonMaxSuppressionV5Options
from .tflite import NotEqualOptions
from .tflite import OneHotOptions
from .tflite import PackOptions
from .tflite import PadOptions
from .tflite import PadV2Options
from .tflite import Pool2DOptions
from .tflite import PowOptions
from .tflite import QuantizeOptions
from .tflite import RangeOptions
from .tflite import RankOptions
from .tflite import ReducerOptions
from .tflite import ReshapeOptions
from .tflite import ResizeBilinearOptions
from .tflite import ResizeNearestNeighborOptions
from .tflite import ReverseSequenceOptions
from .tflite import ReverseV2Options
from .tflite import RNNOptions
from .tflite import ScatterNdOptions
from .tflite import SegmentSumOptions
from .tflite import SelectOptions
from .tflite import SelectV2Options
from .tflite import SequenceRNNOptions
from .tflite import ShapeOptions
from .tflite import SkipGramOptions
from .tflite import SliceOptions
from .tflite import SoftmaxOptions
from .tflite import SpaceToBatchNDOptions
from .tflite import SpaceToDepthOptions
from .tflite import SparseToDenseOptions
from .tflite import SplitOptions
from .tflite import SplitVOptions
from .tflite import SquaredDifferenceOptions
from .tflite import SquareOptions
from .tflite import SqueezeOptions
from .tflite import StridedSliceOptions
from .tflite import SubOptions
from .tflite import SVDFOptions
from .tflite import TileOptions
from .tflite import TopKV2Options
from .tflite import TransposeConvOptions
from .tflite import TransposeOptions
from .tflite import UnidirectionalSequenceLSTMOptions
from .tflite import UniqueOptions
from .tflite import UnpackOptions
from .tflite import WhereOptions
from .tflite import WhileOptions
from .tflite import ZerosLikeOptions
from .tflite.ActivationFunctionType import ActivationFunctionType
from .tflite.BuiltinOperator import BuiltinOperator
from .tflite.BuiltinOptions import BuiltinOptions
from .tflite.Padding import Padding
from .tflite.TensorType import TensorType


def inverse_map(map):
    return {v: k for k, v in map.items()}


datatype_map = {
    TensorType.UINT8: DataType.uint8,
    TensorType.INT8: DataType.int8,
    TensorType.INT16: DataType.int16,
    TensorType.INT32: DataType.int32,
    TensorType.INT64: DataType.int64,
    TensorType.FLOAT16: DataType.float16,
    TensorType.FLOAT32: DataType.float32,
    TensorType.STRING: DataType.string,
    TensorType.BOOL: DataType.bool,
    TensorType.COMPLEX64: DataType.complex64,
}

datatype_inv_map = inverse_map(datatype_map)
datatype_inv_map[DataType.quint8] = TensorType.UINT8

datatype_inv_map[DataType.qint8] = TensorType.INT8
datatype_inv_map[DataType.qint16] = TensorType.INT16
datatype_inv_map[DataType.qint32] = TensorType.INT32


datatype_map_numpy = {
    TensorType.UINT8: np.uint8,
    TensorType.INT8: np.int8,
    TensorType.INT16: np.int16,
    TensorType.INT32: np.int32,
    TensorType.INT64: np.int64,
    TensorType.FLOAT16: np.float16,
    TensorType.FLOAT32: np.float32,
    TensorType.BOOL: np.bool,
    TensorType.COMPLEX64: np.complex64,
}


builtin_options_map = {
    BuiltinOptions.Conv2DOptions: Conv2DOptions.Conv2DOptions,
    BuiltinOptions.DepthwiseConv2DOptions: DepthwiseConv2DOptions.DepthwiseConv2DOptions,
    BuiltinOptions.ConcatEmbeddingsOptions: ConcatEmbeddingsOptions.ConcatEmbeddingsOptions,
    BuiltinOptions.LSHProjectionOptions: LSHProjectionOptions.LSHProjectionOptions,
    BuiltinOptions.Pool2DOptions: Pool2DOptions.Pool2DOptions,
    BuiltinOptions.SVDFOptions: SVDFOptions.SVDFOptions,
    BuiltinOptions.RNNOptions: RNNOptions.RNNOptions,
    BuiltinOptions.FullyConnectedOptions: FullyConnectedOptions.FullyConnectedOptions,
    BuiltinOptions.SoftmaxOptions: SoftmaxOptions.SoftmaxOptions,
    BuiltinOptions.ConcatenationOptions: ConcatenationOptions.ConcatenationOptions,
    BuiltinOptions.AddOptions: AddOptions.AddOptions,
    BuiltinOptions.L2NormOptions: L2NormOptions.L2NormOptions,
    BuiltinOptions.LocalResponseNormalizationOptions: LocalResponseNormalizationOptions.LocalResponseNormalizationOptions,  # noqa: E501
    BuiltinOptions.LSTMOptions: LSTMOptions.LSTMOptions,
    BuiltinOptions.ResizeBilinearOptions: ResizeBilinearOptions.ResizeBilinearOptions,
    BuiltinOptions.CallOptions: CallOptions.CallOptions,
    BuiltinOptions.ReshapeOptions: ReshapeOptions.ReshapeOptions,
    BuiltinOptions.SkipGramOptions: SkipGramOptions.SkipGramOptions,
    BuiltinOptions.SpaceToDepthOptions: SpaceToDepthOptions.SpaceToDepthOptions,
    BuiltinOptions.EmbeddingLookupSparseOptions: EmbeddingLookupSparseOptions.EmbeddingLookupSparseOptions,
    BuiltinOptions.MulOptions: MulOptions.MulOptions,
    BuiltinOptions.PadOptions: PadOptions.PadOptions,
    BuiltinOptions.GatherOptions: GatherOptions.GatherOptions,
    BuiltinOptions.BatchToSpaceNDOptions: BatchToSpaceNDOptions.BatchToSpaceNDOptions,
    BuiltinOptions.SpaceToBatchNDOptions: SpaceToBatchNDOptions.SpaceToBatchNDOptions,
    BuiltinOptions.TransposeOptions: TransposeOptions.TransposeOptions,
    BuiltinOptions.ReducerOptions: ReducerOptions.ReducerOptions,
    BuiltinOptions.SubOptions: SubOptions.SubOptions,
    BuiltinOptions.DivOptions: DivOptions.DivOptions,
    BuiltinOptions.SqueezeOptions: SqueezeOptions.SqueezeOptions,
    BuiltinOptions.SequenceRNNOptions: SequenceRNNOptions.SequenceRNNOptions,
    BuiltinOptions.StridedSliceOptions: StridedSliceOptions.StridedSliceOptions,
    BuiltinOptions.ExpOptions: ExpOptions.ExpOptions,
    BuiltinOptions.TopKV2Options: TopKV2Options.TopKV2Options,
    BuiltinOptions.SplitOptions: SplitOptions.SplitOptions,
    BuiltinOptions.LogSoftmaxOptions: LogSoftmaxOptions.LogSoftmaxOptions,
    BuiltinOptions.CastOptions: CastOptions.CastOptions,
    BuiltinOptions.DequantizeOptions: DequantizeOptions.DequantizeOptions,
    BuiltinOptions.MaximumMinimumOptions: MaximumMinimumOptions.MaximumMinimumOptions,
    BuiltinOptions.ArgMaxOptions: ArgMaxOptions.ArgMaxOptions,
    BuiltinOptions.LessOptions: LessOptions.LessOptions,
    BuiltinOptions.NegOptions: NegOptions.NegOptions,
    BuiltinOptions.PadV2Options: PadV2Options.PadV2Options,
    BuiltinOptions.GreaterOptions: GreaterOptions.GreaterOptions,
    BuiltinOptions.GreaterEqualOptions: GreaterEqualOptions.GreaterEqualOptions,
    BuiltinOptions.LessEqualOptions: LessEqualOptions.LessEqualOptions,
    BuiltinOptions.SelectOptions: SelectOptions.SelectOptions,
    BuiltinOptions.SliceOptions: SliceOptions.SliceOptions,
    BuiltinOptions.TransposeConvOptions: TransposeConvOptions.TransposeConvOptions,
    BuiltinOptions.SparseToDenseOptions: SparseToDenseOptions.SparseToDenseOptions,
    BuiltinOptions.TileOptions: TileOptions.TileOptions,
    BuiltinOptions.ExpandDimsOptions: ExpandDimsOptions.ExpandDimsOptions,
    BuiltinOptions.EqualOptions: EqualOptions.EqualOptions,
    BuiltinOptions.NotEqualOptions: NotEqualOptions.NotEqualOptions,
    BuiltinOptions.ShapeOptions: ShapeOptions.ShapeOptions,
    BuiltinOptions.PowOptions: PowOptions.PowOptions,
    BuiltinOptions.ArgMinOptions: ArgMinOptions.ArgMinOptions,
    BuiltinOptions.FakeQuantOptions: FakeQuantOptions.FakeQuantOptions,
    BuiltinOptions.PackOptions: PackOptions.PackOptions,
    BuiltinOptions.LogicalOrOptions: LogicalOrOptions.LogicalOrOptions,
    BuiltinOptions.OneHotOptions: OneHotOptions.OneHotOptions,
    BuiltinOptions.LogicalAndOptions: LogicalAndOptions.LogicalAndOptions,
    BuiltinOptions.LogicalNotOptions: LogicalNotOptions.LogicalNotOptions,
    BuiltinOptions.UnpackOptions: UnpackOptions.UnpackOptions,
    BuiltinOptions.FloorDivOptions: FloorDivOptions.FloorDivOptions,
    BuiltinOptions.SquareOptions: SquareOptions.SquareOptions,
    BuiltinOptions.ZerosLikeOptions: ZerosLikeOptions.ZerosLikeOptions,
    BuiltinOptions.FillOptions: FillOptions.FillOptions,
    BuiltinOptions.BidirectionalSequenceLSTMOptions: BidirectionalSequenceLSTMOptions.BidirectionalSequenceLSTMOptions,
    BuiltinOptions.BidirectionalSequenceRNNOptions: BidirectionalSequenceRNNOptions.BidirectionalSequenceRNNOptions,
    BuiltinOptions.UnidirectionalSequenceLSTMOptions: UnidirectionalSequenceLSTMOptions.UnidirectionalSequenceLSTMOptions,  # noqa: E501
    BuiltinOptions.FloorModOptions: FloorModOptions.FloorModOptions,
    BuiltinOptions.RangeOptions: RangeOptions.RangeOptions,
    BuiltinOptions.ResizeNearestNeighborOptions: ResizeNearestNeighborOptions.ResizeNearestNeighborOptions,
    BuiltinOptions.LeakyReluOptions: LeakyReluOptions.LeakyReluOptions,
    BuiltinOptions.SquaredDifferenceOptions: SquaredDifferenceOptions.SquaredDifferenceOptions,
    BuiltinOptions.MirrorPadOptions: MirrorPadOptions.MirrorPadOptions,
    BuiltinOptions.AbsOptions: AbsOptions.AbsOptions,
    BuiltinOptions.SplitVOptions: SplitVOptions.SplitVOptions,
    BuiltinOptions.UniqueOptions: UniqueOptions.UniqueOptions,
    BuiltinOptions.ReverseV2Options: ReverseV2Options.ReverseV2Options,
    BuiltinOptions.AddNOptions: AddNOptions.AddNOptions,
    BuiltinOptions.GatherNdOptions: GatherNdOptions.GatherNdOptions,
    BuiltinOptions.CosOptions: CosOptions.CosOptions,
    BuiltinOptions.WhereOptions: WhereOptions.WhereOptions,
    BuiltinOptions.RankOptions: RankOptions.RankOptions,
    BuiltinOptions.ReverseSequenceOptions: ReverseSequenceOptions.ReverseSequenceOptions,
    BuiltinOptions.MatrixDiagOptions: MatrixDiagOptions.MatrixDiagOptions,
    BuiltinOptions.QuantizeOptions: QuantizeOptions.QuantizeOptions,
    BuiltinOptions.MatrixSetDiagOptions: MatrixSetDiagOptions.MatrixSetDiagOptions,
    BuiltinOptions.DensifyOptions: DensifyOptions.DensifyOptions,
    BuiltinOptions.DepthToSpaceOptions: DepthToSpaceOptions.DepthToSpaceOptions,
    BuiltinOptions.HardSwishOptions: HardSwishOptions.HardSwishOptions,
    BuiltinOptions.IfOptions: IfOptions.IfOptions,
    BuiltinOptions.NonMaxSuppressionV4Options: NonMaxSuppressionV4Options.NonMaxSuppressionV4Options,
    BuiltinOptions.NonMaxSuppressionV5Options: NonMaxSuppressionV5Options.NonMaxSuppressionV5Options,
    BuiltinOptions.ScatterNdOptions: ScatterNdOptions.ScatterNdOptions,
    BuiltinOptions.SegmentSumOptions: SegmentSumOptions.SegmentSumOptions,
    BuiltinOptions.SelectV2Options: SelectV2Options.SelectV2Options,
    BuiltinOptions.WhileOptions: WhileOptions.WhileOptions,
}

builtin_options_inv_map = inverse_map(builtin_options_map)


def underscore_to_camel_case(s):
    return "".join(x.title() for x in s.split("_"))


def padding_deserialize(x):
    return padding_map[x]


def padding_serialize(builder, x):
    return padding_inv_map[x]


def activation_deserialize(x):
    return activation_function_map[x]


def activation_serialize(builder, x):
    return activation_function_inv_map[x]


def datatype_deserialize(x):
    return datatype_map[x]


def datatype_serialize(builder, x):
    return datatype_inv_map[x]


def identity(x):
    return x


def identity_serialize(builder, x):
    return x


def write_byte_vector(builder, v):
    builder.StartVector(1, len(v), 1)
    for e in v[::-1]:
        builder.PrependByte(e)
    return builder.EndVector(len(v))


def write_int_vector(builder, v):
    builder.StartVector(4, len(v), 4)
    for e in v[::-1]:
        builder.PrependInt32(e)
    return builder.EndVector(len(v))


class OptionsSerializer:
    def __init__(self, name, members=[]):
        self.name = name
        self.module = globals()[self.name]
        self.cls = getattr(self.module, self.name)
        self.builtin_opt_type = builtin_options_inv_map[self.cls]
        self.members = []
        for mem in members:
            deserialize = identity
            serialize = identity_serialize
            is_vector = False
            if isinstance(mem, tuple):
                if len(mem) == 3:
                    mem, deserialize, serialize = mem
                elif len(mem) == 2:
                    mem, is_vector = mem
                    deserialize = tuple
                    serialize = write_int_vector
                else:
                    assert 0
            underscore_mem = mem
            camelcase_mem = underscore_to_camel_case(mem)
            self.members.append((underscore_mem, camelcase_mem, deserialize, serialize, is_vector))

    def deserialize(self, op_data):
        builtin_options = op_data.BuiltinOptions()
        attrs = {}
        if builtin_options:
            tfattrs = self.cls()
            tfattrs.Init(builtin_options.Bytes, builtin_options.Pos)
            for underscore_mem, camelcase_mem, deserialize, serialize, is_vector in self.members:
                fun = camelcase_mem
                if is_vector:
                    fun += "AsNumpy"

                a = deserialize(getattr(tfattrs, fun)())
                attrs[underscore_mem] = a
        return attrs

    def serialize(self, builder, attrs):
        ser_attrs = []
        for underscore_mem, camelcase_mem, deserialize, serialize, is_vector in self.members:
            a = serialize(builder, attrs[underscore_mem])
            ser_attrs.append((camelcase_mem, a))

        getattr(self.module, self.name + "Start")(builder)

        for camelcase_mem, a in ser_attrs:
            getattr(self.module, self.name + "Add" + camelcase_mem)(builder, a)

        return getattr(self.module, self.name + "End")(builder), None


class CustomOptionsSerializer:
    CUSTOM_OPTIONS_NPU_OP = [0x01, 0x04, 0x01]  # NpuOp=1, FlexbufferFormat.UINT8=4, byte length=1
    CUSTOM_OPTIONS_FORMAT_DEFAULT = 0

    def __init__(self):
        self.custom_opt_format = 0

    def deserialize(self, op_data):
        attrs = {}
        custom_options = op_data.CustomOptionsAsNumpy()
        attrs["custom_options"] = custom_options
        attrs["custom_options_format"] = op_data.CustomOptionsFormat()

        if np.array_equal(custom_options, self.CUSTOM_OPTIONS_NPU_OP):
            attrs["custom_type"] = "ExistingNpuOp"

        return attrs

    def serialize(self, builder, attrs):
        custom_type = attrs.get("custom_type", "")
        self.custom_opt_format = attrs.get("custom_options_format", self.CUSTOM_OPTIONS_FORMAT_DEFAULT)

        # Set NPU op custom options for the TensorFlow Lite custom operator
        if custom_type == "NpuOp":
            custom_options = self.CUSTOM_OPTIONS_NPU_OP
        else:
            custom_options = attrs.get("custom_options", [])

        custom_options_bytes = struct.pack("<{0}B".format(len(custom_options)), *custom_options)
        custom_offset = write_byte_vector(builder, custom_options_bytes)

        return None, custom_offset


padding_map = {
    Padding.SAME: b"SAME",
    Padding.VALID: b"VALID",
}

padding_inv_map = inverse_map(padding_map)


activation_function_map = {
    ActivationFunctionType.NONE: None,
    ActivationFunctionType.RELU: "Relu",
    ActivationFunctionType.RELU_N1_TO_1: "ReluN1To1",
    ActivationFunctionType.RELU6: "Relu6",
    ActivationFunctionType.TANH: "Tanh",
    ActivationFunctionType.SIGN_BIT: "SignBit",
}

activation_function_inv_map = inverse_map(activation_function_map)

fused_act = ("fused_activation_function", activation_deserialize, activation_serialize)
padding = ("padding", padding_deserialize, padding_serialize)

pool2d_opts = OptionsSerializer(
    "Pool2DOptions", (padding, "stride_w", "stride_h", "filter_width", "filter_height", fused_act,)
)

depthwise_opts = OptionsSerializer(
    "DepthwiseConv2DOptions",
    (padding, "stride_w", "stride_h", "depth_multiplier", fused_act, "dilation_w_factor", "dilation_h_factor",),
)

conv2d_opts = OptionsSerializer(
    "Conv2DOptions", (padding, "stride_w", "stride_h", fused_act, "dilation_w_factor", "dilation_h_factor",)
)

lstm_opts = OptionsSerializer("LSTMOptions", (fused_act, "cell_clip", "proj_clip", "kernel_type"))

unidir_seq_lstm_opts = OptionsSerializer(
    "UnidirectionalSequenceLSTMOptions", (fused_act, "cell_clip", "proj_clip", "time_major")
)

bidir_seq_lstm_opts = OptionsSerializer(
    "BidirectionalSequenceLSTMOptions", (fused_act, "cell_clip", "proj_clip", "merge_outputs", "time_major")
)

rnn_opts = OptionsSerializer("RNNOptions", (fused_act,))

seq_rnn_opts = OptionsSerializer("SequenceRNNOptions", ("time_major", fused_act,))

bidir_seq_rnn_opts = OptionsSerializer("BidirectionalSequenceRNNOptions", ("time_major", fused_act, "merge_outputs",))


reducer_opts = OptionsSerializer("ReducerOptions", ("keep_dims",))

is_int_vec = True

custom_prefix = "Custom_"

builtin_operator_map = {
    BuiltinOperator.ADD: ("AddAct", OptionsSerializer("AddOptions", (fused_act,))),
    BuiltinOperator.AVERAGE_POOL_2D: ("AvgPoolAct", pool2d_opts),
    BuiltinOperator.CONCATENATION: ("ConcatTFLite", OptionsSerializer("ConcatenationOptions", ("axis", fused_act))),
    BuiltinOperator.CONV_2D: ("Conv2DBiasAct", conv2d_opts),
    BuiltinOperator.DEPTHWISE_CONV_2D: ("DepthwiseConv2dBiasAct", depthwise_opts),
    BuiltinOperator.DEPTH_TO_SPACE: ("DepthToSpace", OptionsSerializer("DepthToSpaceOptions", ("block_size",))),
    BuiltinOperator.DEQUANTIZE: ("Dequantize", OptionsSerializer("DequantizeOptions")),
    BuiltinOperator.EMBEDDING_LOOKUP: (None, None),
    BuiltinOperator.FLOOR: ("Floor", None),
    BuiltinOperator.FULLY_CONNECTED: (
        "FullyConnectedAct",
        OptionsSerializer("FullyConnectedOptions", (fused_act, "weights_format")),
    ),
    BuiltinOperator.HASHTABLE_LOOKUP: (None, None),
    # BuiltinOperator.L2_NORMALIZATION : "L2NormAct",
    BuiltinOperator.L2_POOL_2D: (None, pool2d_opts),
    BuiltinOperator.LOCAL_RESPONSE_NORMALIZATION: (
        "LRN",
        OptionsSerializer("LocalResponseNormalizationOptions", ("radius", "bias", "alpha", "beta")),
    ),
    BuiltinOperator.LOGISTIC: ("Sigmoid", None),
    # BuiltinOperator.LSH_PROJECTION : "",
    BuiltinOperator.LSTM: ("LstmAct", lstm_opts),
    BuiltinOperator.MAX_POOL_2D: ("MaxPool", pool2d_opts),
    BuiltinOperator.MUL: ("MulAct", OptionsSerializer("MulOptions", (fused_act,))),
    BuiltinOperator.RELU: ("Relu", None),
    BuiltinOperator.RELU_N1_TO_1: (None, None),
    BuiltinOperator.RELU6: ("Relu6", None),
    BuiltinOperator.RESHAPE: ("Reshape", OptionsSerializer("ReshapeOptions", (("new_shape", is_int_vec),))),
    BuiltinOperator.RESIZE_BILINEAR: (
        "ResizeBilinear",
        OptionsSerializer("ResizeBilinearOptions", ("align_corners", "half_pixel_centers")),
    ),
    BuiltinOperator.RNN: ("RnnAct", rnn_opts),
    BuiltinOperator.SOFTMAX: ("Softmax", OptionsSerializer("SoftmaxOptions", ("beta",))),
    BuiltinOperator.SPACE_TO_DEPTH: ("SpaceToDepth", OptionsSerializer("SpaceToDepthOptions", ("block_size",))),
    BuiltinOperator.SVDF: ("SvdfAct", OptionsSerializer("SVDFOptions", ("rank", fused_act))),
    BuiltinOperator.TANH: ("Tanh", None),
    # BuiltinOperator.CONCAT_EMBEDDINGS : "",
    # BuiltinOperator.SKIP_GRAM : "",
    # BuiltinOperator.CALL : "",
    BuiltinOperator.EMBEDDING_LOOKUP_SPARSE: (None, OptionsSerializer("EmbeddingLookupSparseOptions", ("combiner",))),
    BuiltinOperator.PAD: ("Pad", OptionsSerializer("PadOptions")),
    BuiltinOperator.UNIDIRECTIONAL_SEQUENCE_RNN: ("UnidirectionalSequenceRnnAct", seq_rnn_opts),
    BuiltinOperator.GATHER: ("GatherV2", OptionsSerializer("GatherOptions", ("axis",))),
    BuiltinOperator.BATCH_TO_SPACE_ND: ("BatchToSpaceND", OptionsSerializer("BatchToSpaceNDOptions")),
    BuiltinOperator.SPACE_TO_BATCH_ND: ("SpaceToBatchND", OptionsSerializer("SpaceToBatchNDOptions")),
    BuiltinOperator.TRANSPOSE: ("Transpose", OptionsSerializer("TransposeOptions")),
    BuiltinOperator.MEAN: ("Mean", None),
    BuiltinOperator.SUB: ("SubAct", OptionsSerializer("SubOptions", (fused_act,))),
    BuiltinOperator.DIV: ("DivAct", OptionsSerializer("DivOptions", (fused_act,))),
    BuiltinOperator.SQUEEZE: ("Squeeze", OptionsSerializer("SqueezeOptions", (("squeeze_dims", is_int_vec),))),
    BuiltinOperator.UNIDIRECTIONAL_SEQUENCE_LSTM: ("UnidirectionalSequenceLstmAct", unidir_seq_lstm_opts),
    BuiltinOperator.STRIDED_SLICE: (
        "StridedSlice",
        OptionsSerializer(
            "StridedSliceOptions", ("begin_mask", "end_mask", "ellipsis_mask", "new_axis_mask", "shrink_axis_mask")
        ),
    ),
    BuiltinOperator.BIDIRECTIONAL_SEQUENCE_RNN: ("BidirectionalSequenceRnnAct", bidir_seq_rnn_opts),
    BuiltinOperator.EXP: ("Exp", OptionsSerializer("ExpOptions")),
    BuiltinOperator.TOPK_V2: ("TopKV2", OptionsSerializer("TopKV2Options")),
    BuiltinOperator.SPLIT: ("Split", OptionsSerializer("SplitOptions", ("num_splits",))),
    BuiltinOperator.LOG_SOFTMAX: ("LogSoftmax", OptionsSerializer("LogSoftmaxOptions")),
    # BuiltinOperator.DELEGATE : "",
    BuiltinOperator.BIDIRECTIONAL_SEQUENCE_LSTM: ("BidirectionalSequenceLstmAct", bidir_seq_lstm_opts),
    BuiltinOperator.CAST: (
        "Cast",
        OptionsSerializer(
            "CastOptions",
            (
                ("in_data_type", datatype_deserialize, datatype_serialize),
                ("out_data_type", datatype_deserialize, datatype_serialize),
            ),
        ),
    ),
    BuiltinOperator.PRELU: ("Prelu", None),
    BuiltinOperator.MAXIMUM: ("Maximum", OptionsSerializer("MaximumMinimumOptions")),
    BuiltinOperator.ARG_MAX: (
        "ArgMax",
        OptionsSerializer("ArgMaxOptions", (("output_type", datatype_deserialize, datatype_serialize),)),
    ),
    BuiltinOperator.MINIMUM: ("Minimum", OptionsSerializer("MaximumMinimumOptions")),
    BuiltinOperator.LESS: ("Less", None),
    BuiltinOperator.NEG: ("Neg", None),
    BuiltinOperator.PADV2: ("PadV2", None),
    BuiltinOperator.GREATER: ("Greater", None),
    BuiltinOperator.GREATER_EQUAL: ("GreaterEqual", None),
    BuiltinOperator.LESS_EQUAL: ("LessEqual", None),
    BuiltinOperator.SELECT: ("Select", None),
    BuiltinOperator.SLICE: ("Slice", None),
    BuiltinOperator.SIN: ("Sin", None),
    BuiltinOperator.TRANSPOSE_CONV: (
        "Conv2DBackpropInput",
        OptionsSerializer("TransposeConvOptions", (padding, "stride_w", "stride_h")),
    ),
    BuiltinOperator.SPARSE_TO_DENSE: (
        "SparseToDense",
        OptionsSerializer("SparseToDenseOptions", ("validate_indices",)),
    ),
    BuiltinOperator.TILE: ("Tile", OptionsSerializer("TileOptions")),
    BuiltinOperator.EXPAND_DIMS: ("ExpandDims", None),
    BuiltinOperator.EQUAL: ("Equal", None),
    BuiltinOperator.NOT_EQUAL: ("NotEqual", None),
    BuiltinOperator.LOG: ("Log", None),
    BuiltinOperator.SUM: ("Sum", None),
    BuiltinOperator.SQRT: ("Sqrt", None),
    BuiltinOperator.RSQRT: ("Rsqrt", None),
    BuiltinOperator.SHAPE: (
        "Shape",
        OptionsSerializer("ShapeOptions", (("out_type", datatype_deserialize, datatype_serialize),)),
    ),
    BuiltinOperator.POW: ("Pow", None),
    BuiltinOperator.ARG_MIN: (
        "ArgMin",
        OptionsSerializer("ArgMinOptions", (("output_type", datatype_deserialize, datatype_serialize),)),
    ),
    BuiltinOperator.FAKE_QUANT: (
        "FakeQuantWithMinMaxArgs",
        OptionsSerializer("FakeQuantOptions", ("min", "max", "num_bits", "narrow_range")),
    ),
    BuiltinOperator.REDUCE_PROD: ("Prod", reducer_opts),
    BuiltinOperator.REDUCE_MAX: ("Max", reducer_opts),
    BuiltinOperator.PACK: ("Pack", OptionsSerializer("PackOptions", ("values_count", "axis"))),
    BuiltinOperator.LOGICAL_OR: ("LogicalOr", None),
    BuiltinOperator.ONE_HOT: ("OneHot", OptionsSerializer("OneHotOptions", ("axis",))),
    BuiltinOperator.LOGICAL_AND: ("LogicalAnd", None),
    BuiltinOperator.LOGICAL_NOT: ("LogicalNot", None),
    BuiltinOperator.UNPACK: ("Unpack", OptionsSerializer("UnpackOptions", ("num", "axis"))),
    BuiltinOperator.REDUCE_MIN: ("Min", reducer_opts),
    BuiltinOperator.FLOOR_DIV: ("FloorDiv", None),
    BuiltinOperator.REDUCE_ANY: ("Any", reducer_opts),
    BuiltinOperator.SQUARE: ("Square", None),
    BuiltinOperator.ZEROS_LIKE: ("ZerosLike", None),
    BuiltinOperator.FILL: ("Fill", None),
    BuiltinOperator.FLOOR_MOD: ("FloorMod", None),
    BuiltinOperator.RANGE: ("Range", None),
    BuiltinOperator.RESIZE_NEAREST_NEIGHBOR: (
        "ResizeNearestNeighbor",
        OptionsSerializer("ResizeNearestNeighborOptions", ("align_corners",)),
    ),
    BuiltinOperator.LEAKY_RELU: ("LeakyRelu", OptionsSerializer("LeakyReluOptions", ("alpha",))),
    BuiltinOperator.SQUARED_DIFFERENCE: ("SquaredDifference", None),
    BuiltinOperator.MIRROR_PAD: ("MirrorPad", OptionsSerializer("MirrorPadOptions", ("mode",))),
    BuiltinOperator.ABS: ("Abs", None),
    BuiltinOperator.SPLIT_V: ("SplitV", OptionsSerializer("SplitVOptions", ("num_splits",))),
    BuiltinOperator.UNIQUE: (
        "Unique",
        OptionsSerializer("UniqueOptions", (("idx_out_type", datatype_deserialize, datatype_serialize),)),
    ),
    BuiltinOperator.CEIL: ("Ceil", None),
    BuiltinOperator.REVERSE_V2: ("ReverseV2", None),
    BuiltinOperator.ADD_N: ("AddN", None),
    BuiltinOperator.GATHER_ND: ("GatherNd", None),
    BuiltinOperator.COS: ("Cos", None),
    BuiltinOperator.WHERE: ("Where", None),
    BuiltinOperator.RANK: ("Rank", None),
    BuiltinOperator.ELU: ("Elu", None),
    BuiltinOperator.REVERSE_SEQUENCE: (
        "ReverseSequence",
        OptionsSerializer("ReverseSequenceOptions", ("seq_dim", "batch_dim")),
    ),
    BuiltinOperator.MATRIX_DIAG: ("MatrixDiag", None),
    BuiltinOperator.QUANTIZE: ("Quantize", None),
    BuiltinOperator.MATRIX_SET_DIAG: ("MatrixSetDiag", None),
    BuiltinOperator.HARD_SWISH: ("HardSwish", OptionsSerializer("HardSwishOptions")),
    BuiltinOperator.IF: ("If", OptionsSerializer("IfOptions", ("then_subgraph_index", "else_subgraph_index"))),
    BuiltinOperator.WHILE: ("While", OptionsSerializer("WhileOptions", ("cond_subgraph_index", "body_subgraph_index"))),
    BuiltinOperator.NON_MAX_SUPPRESSION_V4: ("NonMaxSuppressionV4", OptionsSerializer("NonMaxSuppressionV4Options")),
    BuiltinOperator.NON_MAX_SUPPRESSION_V5: ("NonMaxSuppressionV5", OptionsSerializer("NonMaxSuppressionV5Options")),
    BuiltinOperator.SCATTER_ND: ("ScatterNd", OptionsSerializer("ScatterNdOptions")),
    BuiltinOperator.SELECT_V2: ("SelectV2", OptionsSerializer("SelectV2Options")),
    BuiltinOperator.DENSIFY: ("Densify", OptionsSerializer("DensifyOptions")),
    BuiltinOperator.SEGMENT_SUM: ("SegmentSum", OptionsSerializer("SegmentSumOptions")),
    BuiltinOperator.CUSTOM: (custom_prefix, CustomOptionsSerializer()),
}

builtin_operator_inv_map = {v[0]: (k, v[1]) for k, v in builtin_operator_map.items()}

builtin_operator_inv_map["NpuOp"] = (BuiltinOperator.CUSTOM, CustomOptionsSerializer())
