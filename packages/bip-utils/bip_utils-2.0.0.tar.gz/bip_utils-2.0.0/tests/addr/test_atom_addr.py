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
    AtomAddr, CosmosConf, BandProtocolConf, BinanceChainConf, IrisNetConf, KavaConf, TerraConf
)
from tests.addr.test_addr_base import AddrBaseTestHelper
from tests.addr.test_addr_const import TEST_SECP256K1_ADDR_INVALID_KEY_TYPES
from tests.ecc.test_ecc import TEST_VECT_SECP256K1_PUB_KEY_INVALID, Secp256k1PublicKey

# Some random public keys
TEST_VECT = [
    {
        "pub_key": b"039cb22e5c6ce15e06b76d5725dcf084b87357d926dcdfeeb20d628d3d11ff543b",
        "addr_params": {"hrp": CosmosConf.ADDR_HRP},
        "address": "cosmos1zewfm2c4s6uv5s4rywksqden8dvya4wmqyyvek",
    },
    {
        "pub_key": b"02dc27af24c0fc6b448519e17d4ac6078f158a766bbf8446cb16c61a9e53835c3c",
        "addr_params": {"hrp": CosmosConf.ADDR_HRP},
        "address": "cosmos1n6ugmlarydek7k8wslzuy55seftfe7g2aqncw3",
    },
    {
        "pub_key": b"0356ab0a0717738c794caf972ee2091762525a35d062c881b863733f06f445c585",
        "addr_params": {"hrp": BandProtocolConf.ADDR_HRP},
        "address": "band16nez6ldt0zp648zgk8g2af50245y0ykjutc2k9",
    },
    {
        "pub_key": b"02b19f4692195f95a8d919edf245d64993bce60bb3c50e4226ba5311686ccf60da",
        "addr_params": {"hrp": BandProtocolConf.ADDR_HRP},
        "address": "band16a3pvl8jmf84uvreek79mta5jr8llmcn4ptgy2",
    },
    {
        "pub_key": b"0356ab0a0717738c794caf972ee2091762525a35d062c881b863733f06f445c585",
        "addr_params": {"hrp": KavaConf.ADDR_HRP},
        "address": "kava16nez6ldt0zp648zgk8g2af50245y0ykje3v4c2",
    },
    {
        "pub_key": b"02b19f4692195f95a8d919edf245d64993bce60bb3c50e4226ba5311686ccf60da",
        "addr_params": {"hrp": KavaConf.ADDR_HRP},
        "address": "kava16a3pvl8jmf84uvreek79mta5jr8llmcnsmlh29",
    },
    {
        "pub_key": b"02ec5dc71723f11e8ed7ae054f1c09110e849edfa491118d161473b78d72cc4813",
        "addr_params": {"hrp": IrisNetConf.ADDR_HRP},
        "address": "iaa1uxgmjgu4eel6fm2ln88ge36y0y4z90c2knr3d6",
    },
    {
        "pub_key": b"02dc27af24c0fc6b448519e17d4ac6078f158a766bbf8446cb16c61a9e53835c3c",
        "addr_params": {"hrp": IrisNetConf.ADDR_HRP},
        "address": "iaa1n6ugmlarydek7k8wslzuy55seftfe7g2gznfvq",
    },
    {
        "pub_key": b"03de159b5635abfdb91b6ae3bf57317d3ecc4eb7a734ef72cc18f307e83359b854",
        "addr_params": {"hrp": TerraConf.ADDR_HRP},
        "address": "terra1tqgahz3c85x438vgeh57z63rs04cshlcx5ga4z",
    },
    {
        "pub_key": b"033e444813a45a334240087619ffc73e626db10454738e08dbdfc71741fb44af26",
        "addr_params": {"hrp": TerraConf.ADDR_HRP},
        "address": "terra1xtdk54kyldfck05je9daej58e87uex0zk47rz5",
    },
    {
        "pub_key": b"0223d645338396fdbce2d754a14568537d52deb76e1addb940994868feef9c5994",
        "addr_params": {"hrp": BinanceChainConf.ADDR_HRP},
        "address": "bnb1lwjdd82uj4fqhu8nqw5d959rhys58dccv9aalj",
    },
    {
        "pub_key": b"03ebbc8a33683fa9d40f4da3b870784d7f66911eec4d464993c2b80d891d452f93",
        "addr_params": {"hrp": BinanceChainConf.ADDR_HRP},
        "address": "bnb16kltf5z0kgm3m7x42h3676xehtpl02csg7f3qc",
    },
]


#
# Tests
#
class AtomAddrTests(unittest.TestCase):
    # Test encode key
    def test_encode_key(self):
        AddrBaseTestHelper.test_encode_key(self, AtomAddr, Secp256k1PublicKey, TEST_VECT)

    # Test invalid keys
    def test_invalid_keys(self):
        AddrBaseTestHelper.test_invalid_keys(self,
                                             AtomAddr,
                                             {"hrp": ""},
                                             TEST_SECP256K1_ADDR_INVALID_KEY_TYPES,
                                             TEST_VECT_SECP256K1_PUB_KEY_INVALID)
