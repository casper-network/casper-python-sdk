import base64
import pathlib
import secrets
import operator
from operator import itemgetter


def test_get_hash(LIB, vectors_2):
    for data, hashes in [operator.itemgetter("data", "hashes")(i) for i in vectors_2]:
        for algo, encoding, digest in [operator.itemgetter("algo", "encoding", "digest")(j) for j in hashes]:
            algo = LIB.crypto.HashAlgorithm[algo]
            encoding = LIB.crypto.HashEncoding[encoding]
            assert digest == LIB.crypto.get_hash(data.encode("utf-8"), 32, algo, encoding)


def test_get_account(LIB, vectors_3):
    for algo, pbk, account_key, accountHash in [operator.itemgetter("algo", "pbk", "accountKey", "accountHash")(i) for i in vectors_3]:
        algo = LIB.crypto.KeyAlgorithm[algo]
        assert algo == LIB.crypto.get_account_key_algo(account_key)
        assert account_key == LIB.crypto.get_account_key(algo, pbk)
        assert LIB.crypto.get_account_hash(account_key) == accountHash


def test_get_key_pair_1(LIB, key_pair_specs):
    """Asserts that a key pair can be generated based upon an algo & encoding.
    
    """
    for key_algo, key_encoding, typeof, pvk_length, pbk_length in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo, key_encoding)
        assert isinstance(pvk, typeof) and len(pvk) == pvk_length
        assert isinstance(pbk, typeof) and len(pbk) == pbk_length
        

def test_get_key_pair_2(LIB, key_pair_specs):
    """Asserts that a key pair can be deserialized from a private key encoded as base64.
    
    """
    for key_algo, key_encoding, _, _, _ in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo, key_encoding)
        pvk_b64 = base64.b64encode(pvk) if key_encoding == LIB.crypto.KeyEncoding.BYTES else \
                  base64.b64encode(bytes.fromhex(pvk))
        assert (pvk, pbk) == LIB.crypto.get_key_pair_from_base64(pvk_b64, key_algo, key_encoding)


def test_get_key_pair_3(LIB, key_pair_specs):
    """Asserts that a key pair can be deserialized from a private key encoded as bytes.
    
    """
    for key_algo, key_encoding, _, _, _ in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo, key_encoding)
        pvk = bytes.fromhex(pvk) if key_encoding == LIB.crypto.KeyEncoding.HEX else pvk
        pvk_pem = LIB.crypto.get_pvk_pem_from_bytes(pvk, key_algo)
        assert isinstance(pvk_pem, bytes)


def test_get_key_pair_4(LIB, key_pair_specs):
    """Asserts that a key pair can be deserialized from a private key encoded as a pem file.
    
    """
    for key_algo, key_encoding, _, _, _ in key_pair_specs:
        pvk, pbk = LIB.crypto.get_key_pair(key_algo, key_encoding)
        if key_encoding == LIB.crypto.KeyEncoding.HEX:
            path_to_pvk_pem_file = LIB.crypto.get_pvk_pem_file_from_bytes(bytes.fromhex(pvk), key_algo)
        else:
            path_to_pvk_pem_file = LIB.crypto.get_pvk_pem_file_from_bytes(pvk, key_algo)
        assert pathlib.Path(path_to_pvk_pem_file).is_file()
        assert (pvk, pbk) == LIB.crypto.get_key_pair_from_pem_file(path_to_pvk_pem_file, key_algo, key_encoding)


def test_get_key_pair_5(LIB, key_pair_specs):
    """Asserts that key pairs can be generated from a seed.
    
    """
    for key_algo, key_encoding, typeof, pvk_length, pbk_length in key_pair_specs:
        seed = secrets.token_bytes(32)
        pvk, pbk = LIB.crypto.get_key_pair_from_bytes(seed, key_algo, key_encoding)
        assert isinstance(pvk, typeof) and len(pvk) == pvk_length
        assert isinstance(pbk, typeof) and len(pbk) == pbk_length


def test_get_public_key_from_private_key_1(LIB, vectors_3):
    """Asserts that a public key can be derived from a private key encoded as a byte array.
    
    """
    for fixture in vectors_3:
        _, pbk = LIB.crypto.get_key_pair_from_bytes(
            bytes.fromhex(fixture["pvk"]),
            LIB.crypto.KeyAlgorithm[fixture["algo"]],
            LIB.crypto.KeyEncoding.HEX
        )
        assert fixture["pbk"] == pbk


def test_get_public_key_from_private_key_2(LIB, vectors_3):
    """Asserts that a public key can be derived from a private key encoded as base64.
    
    """
    for fixture in vectors_3:
        _, pbk = LIB.crypto.get_key_pair_from_base64(
            base64.b64encode(bytes.fromhex(fixture["pvk"])),
            LIB.crypto.KeyAlgorithm[fixture["algo"]],
            LIB.crypto.KeyEncoding.HEX
        )
        assert fixture["pbk"] == pbk


def test_get_public_key_from_private_key_3(LIB, vectors_3):
    """Asserts that a public key can be derived from a private key encoded as hexadecimal.
    
    """
    for fixture in vectors_3:
        _, pbk = LIB.crypto.get_key_pair_from_hex_string(
            fixture["pvk"],
            LIB.crypto.KeyAlgorithm[fixture["algo"]],
            LIB.crypto.KeyEncoding.HEX
        )
        assert fixture["pbk"] == pbk


def test_get_signature(LIB, vectors_4):
    """Asserts that signature algorithms are being correctly executed.
    
    """
    for fixture in vectors_4:
        data = fixture["data"].encode("utf-8")
        key_algo = LIB.crypto.KeyAlgorithm[fixture["signingKey"]["algo"]]
        key_pvk = bytes.fromhex(fixture["signingKey"]["pvk"])
        for sig_info in fixture["signatures"]:
            signature = sig_info["sig"]
            encoding = LIB.crypto.SignatureEncoding[sig_info["encoding"]]
            assert signature == LIB.crypto.get_signature(data, key_pvk, key_algo, encoding)
