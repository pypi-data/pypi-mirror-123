# Copyright (c) 2021 Emanuele Bellocchia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Imports
import unittest
from bip_utils import SolAddr
from tests.addr.test_addr_base import AddrBaseTestHelper
from tests.addr.test_addr_const import TEST_ED25519_ADDR_INVALID_KEY_TYPES
from tests.ecc.test_ecc import TEST_VECT_ED25519_PUB_KEY_INVALID, Ed25519PublicKey

# Some random public keys
TEST_VECT = [
    {
        "pub_key": b"00e9b6062841bb977ad21de71ec961900633c26f21384e015b014a637a61499547",
        "addr_params": {},
        "address": "GjJyeC1r2RgkuoCWMyPYkCWSGSGLcz266EaAkLA27AhL",
    },
    {
        "pub_key": b"008b4564d4b6be05d6ead16d246c5e30773da9459040370284b57c944a3d0a1481",
        "addr_params": {},
        "address": "ANf3TEKFL6jPWjzkndo4CbnNdUNkBk4KHPggJs2nu8Xi",
    },
    {
        "pub_key": b"00dff41688eadfb8574c8fbfeb8707e07ecf571e96e929c395cc506839cc3ef832",
        "addr_params": {},
        "address": "G5DnnAkA9jV3WZ25xh1Z6FcH3vtSyLi6p9nmPpr6dQMX",
    },
    {
        "pub_key": b"e54f392e5ffd3ca8802d3dbaa052667f82f8ff559a9cb23eda39cd386639c6ea",
        "addr_params": {},
        "address": "GS8RquhotKk9sDguxzjg5sJPM8RhfmKXWNEW61Jzjvvu",
    },
    {
        "pub_key": b"6031798a9f0f4939c3335d313848437fe72aefbe0d700de3268a2d45cebedc7c",
        "addr_params": {},
        "address": "7UVttrLkRkZFn4FsTuihX5zCJ1ounF5Ts8CkSqPGN2Dh",
    },
]


#
# Tests
#
class SolAddrTests(unittest.TestCase):
    # Test encode key
    def test_encode_key(self):
        AddrBaseTestHelper.test_encode_key(self, SolAddr, Ed25519PublicKey, TEST_VECT)

    # Test invalid keys
    def test_invalid_keys(self):
        AddrBaseTestHelper.test_invalid_keys(self,
                                             SolAddr,
                                             {},
                                             TEST_ED25519_ADDR_INVALID_KEY_TYPES,
                                             TEST_VECT_ED25519_PUB_KEY_INVALID)
