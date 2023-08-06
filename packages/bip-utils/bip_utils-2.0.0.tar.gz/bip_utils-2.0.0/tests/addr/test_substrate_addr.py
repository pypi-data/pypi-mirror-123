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
from bip_utils import (
    SubstrateEd25519Addr, SubstrateSr25519Addr,
)
from tests.addr.test_addr_base import AddrBaseTestHelper
from tests.addr.test_addr_const import TEST_ED25519_ADDR_INVALID_KEY_TYPES, TEST_SR25519_ADDR_INVALID_KEY_TYPES
from tests.ecc.test_ecc import (
    TEST_VECT_ED25519_PUB_KEY_INVALID, TEST_VECT_SR25519_PUB_KEY_INVALID, Ed25519PublicKey, Sr25519PublicKey
)

# Some random public keys
TEST_VECT = [
    {
        "pub_key": b"46ebddef8cd9bb167dc30878d7113b7e168e6f0646beffd77d69d39bad76b47a",
        "addr_params": {"ss58_format": 0},
        "address": "12bzRJfh7arnnfPPUZHeJUaE62QLEwhK48QnH9LXeK2m1iZU",
    },
    {
        "pub_key": b"e8474b9c29d44d45c0755077d4f8a21dc611c76e36e261773b5410b8e5bf15a1",
        "addr_params": {"ss58_format": 7},
        "address": "nmB6fx6ehzHwA4wyfFVZig28cCAcathGwfShrNsvueitzZC",
    },
    {
        "pub_key": b"8b4564d4b6be05d6ead16d246c5e30773da9459040370284b57c944a3d0a1481",
        "addr_params": {"ss58_format": 18},
        "address": "2rKUvXu7WpfC9VyEvqwVVxxRVKqNp4CgXYwStmfiqqpFAkSC",
    },
    {
        "pub_key": b"8ebb52da3030f06e0c0c5f7d0fbacf6a22cedb1229bb4824a230fbe84bf89304",
        "addr_params": {"ss58_format": 2},
        "address": "FoTxsgYKH4AUngJAJNsqgmK85RzCc6cerkrsN18wiFfwBrn",
    },
    {
        "pub_key": b"e92b4b43a62fa66293f315486d66a67076e860e2aad76acb8e54f9bb7c925cd9",
        "addr_params": {"ss58_format": 42},
        "address": "5HLRsimRtdb11HX73JtRd79avhCMruocgDJUXdosSJK1s6nz",
    },
    {
        "pub_key": b"2b0538c7c738a370385dc9404fbde697e29d1243d7d7f5c5e558bf4be738b82c",
        "addr_params": {"ss58_format": 70},
        "address": "ctpqudSL8v7QCi3dVRZkBK55i6JGLQuyCAxqFsTho4DCMmw87",
    },
]


#
# Tests
#
class SubstrateAddrTests(unittest.TestCase):
    # Test encode key
    def test_encode_key(self):
        AddrBaseTestHelper.test_encode_key(self, SubstrateEd25519Addr, Ed25519PublicKey, TEST_VECT)
        AddrBaseTestHelper.test_encode_key(self, SubstrateSr25519Addr, Sr25519PublicKey, TEST_VECT)

    # Test invalid keys
    def test_invalid_keys(self):
        AddrBaseTestHelper.test_invalid_keys(self,
                                             SubstrateEd25519Addr,
                                             {"ss58_format": 0},
                                             TEST_ED25519_ADDR_INVALID_KEY_TYPES,
                                             TEST_VECT_ED25519_PUB_KEY_INVALID)
        AddrBaseTestHelper.test_invalid_keys(self,
                                             SubstrateSr25519Addr,
                                             {"ss58_format": 0},
                                             TEST_SR25519_ADDR_INVALID_KEY_TYPES,
                                             TEST_VECT_SR25519_PUB_KEY_INVALID)
