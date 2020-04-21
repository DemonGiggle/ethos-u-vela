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
# Serialises and packs an NPU subgraph into tensors.
import struct

import numpy as np

from . import driver_actions
from .data_type import DataType
from .nn_graph import PassPlacement
from .operation import Operation
from .tensor import MemArea
from .tensor import Tensor
from .tensor import TensorFormat
from .tensor import TensorPurpose


def make_memory_tensor(name, mem_area, sz, want_values, arch):
    tens = Tensor([sz], DataType.uint8, name)
    tens.mem_area = mem_area
    tens.purpose = TensorPurpose.FeatureMap
    tens.set_format(TensorFormat.NHWC, arch)
    if want_values:
        tens.values = np.zeros(tens.shape, np.uint8)
    return tens


def copy_compressed_values_to_memory_tensor(memory_tensor, src_tensor):
    start_addr = src_tensor.address
    for compressed_values in src_tensor.compressed_values:
        end_addr = start_addr + len(compressed_values)
        memory_tensor.values[start_addr:end_addr] = compressed_values
        start_addr = end_addr


def serialise_npu_subgraph_into_tensors(nng, sg, arch, scratch_tens, flash_tens):
    if sg.placement != PassPlacement.Npu:
        return scratch_tens, flash_tens

    flash_area = arch.permanent_storage_mem_area
    scratch_area = MemArea.Sram

    flash_size = sg.memory_used.get(flash_area, 0)
    scratch_size = sg.memory_used.get(scratch_area, 0)

    # Prepare driver actions for this command tensor
    da_list = []
    driver_actions.emit_fourcc(da_list, "COP1")
    driver_actions.emit_config(da_list, 0, 1, arch)
    driver_actions.emit_cmd_stream_header(da_list, len(sg.register_command_stream))

    # Append command stream words
    da_list.extend(sg.register_command_stream)

    # Convert to bytes
    payload_bytes = struct.pack("<{0}I".format(len(da_list)), *da_list)

    command_stream_size_bytes = len(payload_bytes)

    # Adjust the bits per element calculation to exclude metadata generated by Vela
    nng.total_size[flash_area] = nng.total_size.get(flash_area, 0) - flash_size - command_stream_size_bytes
    nng.total_elements[flash_area] = nng.total_elements.get(flash_area, 0) - flash_size - command_stream_size_bytes
    nng.total_size[scratch_area] = nng.total_size.get(scratch_area, 0) - scratch_size
    nng.total_elements[scratch_area] = nng.total_elements.get(scratch_area, 0) - scratch_size

    if flash_tens == scratch_tens is None:
        # First Npu subgraph, create scratch and flash tensors
        sg.scratch_tensor = make_memory_tensor(sg.name + "_scratch", scratch_area, scratch_size, False, arch)
        sg.scratch_tensor.purpose = TensorPurpose.Scratch
        sg.flash_tensor = make_memory_tensor(sg.name + "_flash", flash_area, flash_size, True, arch)
    else:
        sg.scratch_tensor = scratch_tens
        sg.scratch_tensor.shape[0] += scratch_size
        sg.flash_tensor = flash_tens
        sg.flash_tensor.shape[0] += flash_size

    for cps in sg.cascaded_passes:
        for ps in cps.passes:
            if ps.placement == PassPlacement.Npu and ps.weight_tensor is not None:
                # For DMA ops, ps.weight_tensor is referring to the SRAM weight tensor and therefore the address
                # is pointing at the destination address of where the weights should be placed in SRAM.
                # This ensures that the Flash weight tensor is used instead and thus gets the correct address.
                if ps.weight_tensor.ops[0].type == "DMA":
                    copy_compressed_values_to_memory_tensor(sg.flash_tensor, ps.weight_tensor.ops[0].inputs[0])
                else:
                    copy_compressed_values_to_memory_tensor(sg.flash_tensor, ps.weight_tensor)

                copy_compressed_values_to_memory_tensor(sg.flash_tensor, ps.scale_tensor)

    sg.command_stream_tensor = make_memory_tensor(
        sg.name + "_command_stream", flash_area, command_stream_size_bytes, True, arch
    )
    sg.command_stream_tensor.values = np.frombuffer(payload_bytes, dtype=np.uint8)

    return sg.scratch_tensor, sg.flash_tensor


def add_const_tens_to_startup_cascaded_pass(startup_cps, tens):
    op = Operation("Const", tens.name + "_const")
    op.outputs = [tens]
    tens.ops = [op]
    startup_cps.passes[0].ops.insert(0, op)
    startup_cps.passes[0].outputs.insert(0, tens)
    startup_cps.outputs.insert(0, tens)


def rewrite_npu_call_ops(nng, sg, arch):
    if sg.placement != PassPlacement.Cpu:
        return

    startup_cps = sg.cascaded_passes[0]

    for idx, cps in enumerate(sg.cascaded_passes):
        for ps in cps.passes:
            for op in ps.ops:
                if op.type == "NpuOp":
                    callee = op.attrs["subgraph"]
                    op.attrs["custom_options"] = {"type": op.type}

                    sz = 0
                    for tens in [callee.scratch_tensor, callee.flash_tensor, callee.command_stream_tensor]:
                        op.inputs.insert(0, tens)
                        ps.inputs.insert(0, tens)
                        cps.inputs.insert(0, tens)
                        if tens != callee.scratch_tensor:
                            add_const_tens_to_startup_cascaded_pass(startup_cps, tens)
                        sz += tens.storage_size()

                    for prev_cps in sg.cascaded_passes[: idx + 1]:
                        prev_cps.sram_used += sz

                    if callee.scratch_tensor is not None:
                        cps.sram_used += callee.scratch_tensor.storage_size()
