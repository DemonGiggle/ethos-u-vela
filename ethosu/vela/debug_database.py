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
import csv
import io
from typing import Any
from typing import Dict
from typing import List

import lxml.etree as xml

from . import numeric_util
from .operation import Operation

UntypedDict = Dict[Any, Any]
UntypedList = List[Any]


class DebugDatabase:
    NULLREF = -1
    show_warnings = False

    SOURCE_TABLE = "source"
    _sourceUID: UntypedDict = {}
    _sourceHeaders = ["id", "operator", "kernel_w", "kernel_h", "ofm_w", "ofm_h", "ofm_d"]
    _sourceTable: UntypedList = []

    OPTIMISED_TABLE = "optimised"
    _optimisedUID: UntypedDict = {}
    _optimisedHeaders = ["id", "source_id", "operator", "kernel_w", "kernel_h", "ofm_w", "ofm_h", "ofm_d"]
    _optimisedTable: UntypedList = []

    QUEUE_TABLE = "queue"
    _queueHeaders = ["offset", "cmdstream_id", "optimised_id"]
    _queueTable: UntypedList = []

    STREAM_TABLE = "cmdstream"
    _streamUID: UntypedDict = {}
    _streamHeaders = ["id", "file_offset"]
    _streamTable: UntypedList = []

    @classmethod
    def add_source(cls, op: Operation):
        assert isinstance(op, Operation)
        uid = len(cls._sourceUID)
        cls._sourceUID[op] = uid
        ofm_shape = numeric_util.full_shape(3, op.outputs[0].shape, 1)
        cls._sourceTable.append(
            [uid, op.type, op.kernel.width, op.kernel.height, ofm_shape[-2], ofm_shape[-3], ofm_shape[-1]]
        )

    @classmethod
    def add_optimised(cls, parent: Operation, op: Operation):
        assert isinstance(parent, Operation) and isinstance(op, Operation)
        if op not in cls._optimisedUID:
            if parent not in cls._sourceUID:
                # The the parent wasn't in the source network try to look it
                # up in the optimised network and use that op's source parent.
                if parent in cls._optimisedUID:
                    src_uid = cls._optimisedUID[parent][1]
                else:
                    if DebugDatabase.show_warnings:
                        print("Debug Database: Associated parent '{0}' not in network".format(parent.type))
                    src_uid = DebugDatabase.NULLREF
            else:
                src_uid = cls._sourceUID[parent]
            uid = len(cls._optimisedUID)
            cls._optimisedUID[op] = (uid, src_uid)
            ofm_shape = numeric_util.full_shape(3, op.outputs[0].shape, 1)
            cls._optimisedTable.append(
                [uid, src_uid, op.type, op.kernel.width, op.kernel.height, ofm_shape[-2], ofm_shape[-3], ofm_shape[-1]]
            )

    @classmethod
    def add_stream(cls, key):
        if key not in cls._streamUID:
            uid = len(cls._streamUID)
            cls._streamUID[key] = uid
        return uid

    @classmethod
    def set_stream_offset(cls, key, file_offset):
        assert key in cls._streamUID
        uid = cls._streamUID[key]
        cls._streamTable.append([uid, file_offset])

    @classmethod
    def add_command(cls, stream_id, offset, op: Operation):
        assert stream_id < len(cls._streamUID)
        assert op in cls._optimisedUID, "Optimised operator must exist before code generation"
        optimised_id = cls._optimisedUID[op][0]
        cls._queueTable.append([offset, stream_id, optimised_id])

    @classmethod
    def _write_table(cls, root, name, headers, table):
        # Convert table to CSV
        out = io.StringIO()
        writer = csv.writer(out, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        writer.writerows(table)

        # Package table into XML output
        table = xml.SubElement(root, "table", {"name": name})
        table.text = xml.CDATA(out.getvalue())

    @classmethod
    def write(cls, file_path, input_file, output_file):
        root = xml.Element("debug", {"source": input_file, "optimised": output_file})

        cls._write_table(root, cls.SOURCE_TABLE, cls._sourceHeaders, cls._sourceTable)
        cls._write_table(root, cls.OPTIMISED_TABLE, cls._optimisedHeaders, cls._optimisedTable)
        cls._write_table(root, cls.QUEUE_TABLE, cls._queueHeaders, cls._queueTable)
        cls._write_table(root, cls.STREAM_TABLE, cls._streamHeaders, cls._streamTable)

        xml.ElementTree(root).write(file_path, encoding="utf-8", xml_declaration=True, pretty_print=True)
