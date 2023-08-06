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
import binascii
import unittest
from bip_utils import (
    Sr25519PublicKey, Sr25519PrivateKey, SubstrateKeyError, SubstratePrivateKey, SubstratePublicKey
)
from bip_utils.substrate.conf.substrate_conf import SubstratePolkadot
from tests.ecc.test_ecc import (
    TEST_VECT_SR25519_PRIV_KEY_INVALID, TEST_VECT_SR25519_PUB_KEY_INVALID,
    TEST_ED25519_PRIV_KEY, TEST_ED25519_BLAKE2B_PRIV_KEY, TEST_ED25519_MONERO_PRIV_KEY, TEST_NIST256P1_PRIV_KEY, TEST_SECP256K1_PRIV_KEY,
    TEST_ED25519_PUB_KEY, TEST_ED25519_BLAKE2B_PUB_KEY, TEST_ED25519_MONERO_PUB_KEY, TEST_NIST256P1_PUB_KEY, TEST_SECP256K1_PUB_KEY,
    TEST_SR25519_PRIV_KEY, TEST_SR25519_PUB_KEY,
)

# Test address
TEST_ADDRESS = "13KVd4f2a4S5pLp4gTTFezyXdPWx27vQ9vS6xBXJ9yWVd7xo"


#
# Tests
#
class SubstrateKeysTests(unittest.TestCase):
    # Test private key
    def test_priv_key(self):
        # FromBytesOrKeyObject (object)
        self.__test_priv_key_obj(SubstratePrivateKey.FromBytesOrKeyObject(TEST_SR25519_PRIV_KEY, SubstratePolkadot))
        # FromBytesOrKeyObject (bytes)
        self.__test_priv_key_obj(SubstratePrivateKey.FromBytesOrKeyObject(TEST_SR25519_PRIV_KEY.Raw().ToBytes(), SubstratePolkadot))
        # FromBytes
        self.__test_priv_key_obj(SubstratePrivateKey.FromBytes(TEST_SR25519_PRIV_KEY.Raw().ToBytes(), SubstratePolkadot))

    # Test public key
    def test_pub_key(self):
        # FromBytesOrKeyObject (object)
        self.__test_pub_key_obj(SubstratePublicKey.FromBytesOrKeyObject(TEST_SR25519_PUB_KEY, SubstratePolkadot))
        # FromBytesOrKeyObject (compressed)
        self.__test_pub_key_obj(SubstratePublicKey.FromBytesOrKeyObject(TEST_SR25519_PUB_KEY.RawCompressed().ToBytes(), SubstratePolkadot))
        # FromBytesOrKeyObject (uncompressed)
        self.__test_pub_key_obj(SubstratePublicKey.FromBytesOrKeyObject(TEST_SR25519_PUB_KEY.RawUncompressed().ToBytes(), SubstratePolkadot))
        # FromBytes (compressed)
        self.__test_pub_key_obj(SubstratePublicKey.FromBytes(TEST_SR25519_PUB_KEY.RawCompressed().ToBytes(), SubstratePolkadot))
        # FromBytes (uncompressed)
        self.__test_pub_key_obj(SubstratePublicKey.FromBytes(TEST_SR25519_PUB_KEY.RawUncompressed().ToBytes(), SubstratePolkadot))

    # Test invalid parameters
    def test_invalid_params(self):
        self.assertRaises(TypeError, SubstratePrivateKey, TEST_ED25519_PRIV_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePrivateKey, TEST_ED25519_BLAKE2B_PRIV_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePrivateKey, TEST_ED25519_MONERO_PRIV_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePrivateKey, TEST_NIST256P1_PRIV_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePrivateKey, TEST_SECP256K1_PRIV_KEY, SubstratePolkadot)

        self.assertRaises(TypeError, SubstratePublicKey, TEST_ED25519_PUB_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePublicKey, TEST_ED25519_BLAKE2B_PUB_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePublicKey, TEST_ED25519_MONERO_PUB_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePublicKey, TEST_NIST256P1_PUB_KEY, SubstratePolkadot)
        self.assertRaises(TypeError, SubstratePublicKey, TEST_SECP256K1_PUB_KEY, SubstratePolkadot)

    # Test invalid keys
    def test_invalid_keys(self):
        # Invalid private keys
        for test in TEST_VECT_SR25519_PRIV_KEY_INVALID:
            self.assertRaises(SubstrateKeyError, SubstratePrivateKey.FromBytesOrKeyObject, binascii.unhexlify(test), SubstratePolkadot)
            self.assertRaises(SubstrateKeyError, SubstratePrivateKey.FromBytes, binascii.unhexlify(test), SubstratePolkadot)
        # Invalid public keys
        for test in TEST_VECT_SR25519_PUB_KEY_INVALID:
            self.assertRaises(SubstrateKeyError, SubstratePublicKey.FromBytesOrKeyObject, binascii.unhexlify(test), SubstratePolkadot)
            self.assertRaises(SubstrateKeyError, SubstratePublicKey.FromBytes, binascii.unhexlify(test), SubstratePolkadot)

    # Test private key object
    def __test_priv_key_obj(self, priv_key):
        self.assertEqual(TEST_SR25519_PRIV_KEY.Raw().ToBytes(), priv_key.Raw().ToBytes())
        self.assertEqual(TEST_SR25519_PRIV_KEY.Raw().ToBytes(), bytes(priv_key.Raw()))
        self.assertEqual(TEST_SR25519_PRIV_KEY.Raw().ToHex(), priv_key.Raw().ToHex())
        self.assertEqual(TEST_SR25519_PRIV_KEY.Raw().ToHex(), str(priv_key.Raw()))

        self.assertTrue(isinstance(priv_key.KeyObject(), Sr25519PrivateKey))
        # Public key associated to the private one
        self.__test_pub_key_obj(priv_key.PublicKey())

    # Test public key object
    def __test_pub_key_obj(self, pub_key):
        self.assertEqual(TEST_SR25519_PUB_KEY.RawCompressed().ToBytes(), pub_key.RawCompressed().ToBytes())
        self.assertEqual(TEST_SR25519_PUB_KEY.RawCompressed().ToBytes(), bytes(pub_key.RawCompressed()))
        self.assertEqual(TEST_SR25519_PUB_KEY.RawCompressed().ToHex(), pub_key.RawCompressed().ToHex())
        self.assertEqual(TEST_SR25519_PUB_KEY.RawCompressed().ToHex(), str(pub_key.RawCompressed()))

        self.assertEqual(TEST_SR25519_PUB_KEY.RawUncompressed().ToBytes(), pub_key.RawUncompressed().ToBytes())
        self.assertEqual(TEST_SR25519_PUB_KEY.RawUncompressed().ToBytes(), bytes(pub_key.RawUncompressed()))
        self.assertEqual(TEST_SR25519_PUB_KEY.RawUncompressed().ToHex(), pub_key.RawUncompressed().ToHex())
        self.assertEqual(TEST_SR25519_PUB_KEY.RawUncompressed().ToHex(), str(pub_key.RawUncompressed()))

        self.assertEqual(TEST_ADDRESS, pub_key.ToAddress())

        self.assertTrue(isinstance(pub_key.KeyObject(), Sr25519PublicKey))
