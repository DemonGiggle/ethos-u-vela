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
# Creates driver actions that are embedded in the custom operator payload.
from typing import List

import numpy as np

from .ethos_u55_regs.ethos_u55_regs import ARCH_VER
from .ethos_u55_regs.ethos_u55_regs import config_r
from .ethos_u55_regs.ethos_u55_regs import id_r


class DACommands:
    Reserved = 0x00
    Config = 0x01
    Config_PatchShift = 4
    CmdStream = 0x02
    ReadAPB = 0x03
    ReadAPB_CountShift = 12
    ReadAPB_IndexMask = (1 << ReadAPB_CountShift) - 1
    DumpSHRAM = 0x04
    NOP = 0x05


def make_da_tag(id: int, reserved: int, param: int) -> int:
    tag: int = id
    tag |= reserved << 8
    tag |= param << 16
    return tag


def emit_fourcc(data: List[int], fourcc: str):
    assert data is not None
    assert fourcc is not None
    assert len(fourcc) == 4
    value: int = 0
    value = fourcc[0].encode()[0]
    value |= fourcc[1].encode()[0] << 8
    value |= fourcc[2].encode()[0] << 16
    value |= fourcc[3].encode()[0] << 24
    data.append(value)


def build_id_word():
    arch_major_rev, arch_minor_rev, arch_patch_rev = (int(x) for x in ARCH_VER.split("."))
    n = id_r()
    n.set_arch_major_rev(arch_major_rev)
    n.set_arch_minor_rev(arch_minor_rev)
    n.set_arch_patch_rev(arch_patch_rev)
    return n.word


def build_config_word(arch):
    macs_cc = arch.config.macs
    log2_macs_cc = int(np.log2(macs_cc) + 0.5)
    shram_size = int(arch.shram_size_bytes / 1024)
    n = config_r()
    n.set_shram_size(shram_size)
    n.set_cmd_stream_version(0)  # may be incremented in the future
    n.set_macs_per_cc(log2_macs_cc)
    return n.word


def emit_config(data: List[int], rel: int, patch: int, arch):
    assert data is not None
    data.append(make_da_tag(DACommands.Config, 0, (patch << DACommands.Config_PatchShift) | rel))
    data.append(build_config_word(arch))
    data.append(build_id_word())


def emit_cmd_stream_header(data: List[int], length: int):
    assert data is not None
    # Insert NOPs to align start of command stream to 16 bytes
    num_nops = 4 - ((len(data) + 1) % 4)
    for _ in range(num_nops):
        data.append(make_da_tag(DACommands.NOP, 0, 0))

    # Use the reserved 8 bit as the length high
    length_high = (length & 0x00FF0000) >> 16
    length_low = length & 0x0000FFFF
    data.append(make_da_tag(DACommands.CmdStream, length_high, length_low))


def emit_reg_read(data: List[int], reg_index: int, reg_count: int = 1):
    assert data is not None
    assert reg_index >= 0
    assert reg_count >= 1
    payload: int = (reg_index & DACommands.ReadAPB_IndexMask) | ((reg_count << DACommands.ReadAPB_CountShift) - 1)
    data.append(make_da_tag(DACommands.ReadAPB, 0, payload))


def emit_dump_shram(data: List[int]):
    assert data is not None
    data.append(make_da_tag(DACommands.DumpSHRAM, 0, 0))
