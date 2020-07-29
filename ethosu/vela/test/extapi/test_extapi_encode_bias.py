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
# Contains unit tests for encode_biases API for an external consumer
import random

import numpy as np

from ethosu.vela.weight_compressor import encode_bias


def test_encode_bias():
    bias_lower_limit = -(1 << (40 - 1))
    bias_upper_limit = (1 << (40 - 1)) - 1
    scale_lower_limit = 0
    scale_upper_limit = (1 << 32) - 1
    shift_lower_limit = 0
    shift_upper_limit = (1 << 6) - 1

    for _ in range(30):
        bias = np.int64(random.randint(bias_lower_limit, bias_upper_limit))
        scale = int(random.randint(scale_lower_limit, scale_upper_limit))
        shift = int(random.randint(shift_lower_limit, shift_upper_limit))
        biases_enc = encode_bias(bias, scale, shift)
        assert isinstance(biases_enc, bytearray)
        assert len(biases_enc) == 10


if __name__ == "__main__":
    test_encode_bias()
