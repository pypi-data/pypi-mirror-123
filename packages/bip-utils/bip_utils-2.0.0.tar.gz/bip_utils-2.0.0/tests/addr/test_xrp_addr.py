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
from bip_utils import XrpAddr
from tests.addr.test_addr_base import AddrBaseTestHelper
from tests.addr.test_addr_const import TEST_SECP256K1_ADDR_INVALID_KEY_TYPES
from tests.ecc.test_ecc import TEST_VECT_SECP256K1_PUB_KEY_INVALID, Secp256k1PublicKey

# Some random public keys
TEST_VECT = [
    {
        "pub_key": b"03db0da69187edd94aba300f1b2e7a09f407a8301d6fff54322a6ee4dde9842681",
        "addr_params": {},
        "address": "rwypvr27pYpzYQyDrFQBjDUhRDkHiecTHo",
    },
    {
        "pub_key": b"03333f37539bf526280cea9dda98758de4feb15910218e3e0a99ac17d1f5fac406",
        "addr_params": {},
        "address": "rLynFggnosDyDmoLzcgX6siu6X4yUBb36a",
    },
    {
        "pub_key": b"02553f6711f6ed3e1204dff91d9bf259ea01a2577dcc05383ce47f2cc5a98946bc",
        "addr_params": {},
        "address": "rJ6twS2cq28qMybswjQHb6BZK7kuwSFfZo",
    },
    {
        "pub_key": b"03530f281debbda165f54090b930c4467842231c3bd2e547d953444c7409ad4c20",
        "addr_params": {},
        "address": "rhs1osifPgg35Ff8pRk23vRtn6rhivVuTq",
    },
    {
        "pub_key": b"021cf750242895325d49efa12859369f7a45e9c3f5639172e4f2f5df4ae23301cf",
        "addr_params": {},
        "address": "rsfsErX3u9GRrMH1Nr6Qa4TAyWa53bx48D",
    },
]


#
# Tests
#
class XrpAddrTests(unittest.TestCase):
    # Test encode key
    def test_encode_key(self):
        AddrBaseTestHelper.test_encode_key(self, XrpAddr, Secp256k1PublicKey, TEST_VECT)

    # Test invalid keys
    def test_invalid_keys(self):
        AddrBaseTestHelper.test_invalid_keys(self,
                                             XrpAddr,
                                             {},
                                             TEST_SECP256K1_ADDR_INVALID_KEY_TYPES,
                                             TEST_VECT_SECP256K1_PUB_KEY_INVALID)
