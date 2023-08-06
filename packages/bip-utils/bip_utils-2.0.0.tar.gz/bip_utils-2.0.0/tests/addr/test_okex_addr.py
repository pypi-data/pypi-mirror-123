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
from bip_utils import OkexAddr
from tests.addr.test_addr_base import AddrBaseTestHelper
from tests.addr.test_addr_const import TEST_SECP256K1_ADDR_INVALID_KEY_TYPES
from tests.ecc.test_ecc import TEST_VECT_SECP256K1_PUB_KEY_INVALID, Secp256k1PublicKey

# Some random public keys
TEST_VECT = [
    {
        "pub_key": b"03baf0b46095920af1a8c636cd9d9df37286190607d44ed82688f62c6c002acbc8",
        "addr_params": {},
        "address": "ex143pr24a30ml64mzgl74fhyuhrwg82y7vmyse7q",
    },
    {
        "pub_key": b"027bba228d456609587ce5d30f63443f421a3b187f6c53c53ba7626568a1025081",
        "addr_params": {},
        "address": "ex1hfh528h34asdtq7t3k7lhsvkhqc32hcypk3gyt",
    },
    {
        "pub_key": b"03ec14157c1bb62c6b8ce10b7379bee621a6f79735b950eaf125913a3da19bdaf9",
        "addr_params": {},
        "address": "ex170k75kvpj4urgs98nnlkhhfz90jrulfkq5k8rn",
    },
    {
        "pub_key": b"03b5f6bafd1656dbd1502b7d941d7bed5cfb2d1b479be9506e92752c96c5145965",
        "addr_params": {},
        "address": "ex1wj4nhg2k54aersyvjrgkv9js4sq74tajsg6zm0",
    },
    {
        "pub_key": b"03068feb64a09aee06eac40abfabd16574e78108948405cc566f175509e17ebb52",
        "addr_params": {},
        "address": "ex1ak63v55f8e765zqk3ucndrzvt29jdjtrkz33f2",
    },
]


#
# Tests
#
class OkexAddrTests(unittest.TestCase):
    # Test encode key
    def test_encode_key(self):
        AddrBaseTestHelper.test_encode_key(self, OkexAddr, Secp256k1PublicKey, TEST_VECT)

    # Test invalid keys
    def test_invalid_keys(self):
        AddrBaseTestHelper.test_invalid_keys(self,
                                             OkexAddr,
                                             {},
                                             TEST_SECP256K1_ADDR_INVALID_KEY_TYPES,
                                             TEST_VECT_SECP256K1_PUB_KEY_INVALID)
