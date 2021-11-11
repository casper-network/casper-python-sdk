import base64
import pathlib
import secrets
import operator

import pycspr


def test_get_hash(crypto_hashes):
    getter_1 = operator.itemgetter("data", "hashes")
    getter_2 = operator.itemgetter("algo", "digest")
    for data, hashes in [getter_1(i) for i in crypto_hashes]:
        for algo, digest in [getter_2(j) for j in hashes]:
            algo = pycspr.crypto.HashAlgorithm[algo]
            assert digest == pycspr.crypto.get_hash(data.encode("utf-8"), 32, algo)


def test_get_account(crypto_key_pairs):
    getter = operator.itemgetter("algo", "pbk", "accountKey", "accountHash")
    for algo, pbk, account_key, accountHash in [getter(i) for i in crypto_key_pairs]:
        algo = pycspr.crypto.KeyAlgorithm[algo]
        assert algo == pycspr.crypto.get_account_key_algo(account_key)
        assert account_key == pycspr.crypto.get_account_key(algo, pbk)
        print(pycspr.crypto.get_account_hash(account_key).hex())
        assert pycspr.crypto.get_account_hash(account_key) == accountHash


def test_that_a_key_pair_can_be_generated(crypto_key_pair_specs):
    for key_algo, pvk_length, pbk_length in crypto_key_pair_specs:
        pvk, pbk = pycspr.crypto.get_key_pair(key_algo)
        assert len(pvk) == pvk_length
        assert len(pbk) == pbk_length


def test_that_a_key_pair_can_be_deserialized_from_base64(crypto_key_pair_specs):
    for key_algo, _, _ in crypto_key_pair_specs:
        pvk, pbk = pycspr.crypto.get_key_pair(key_algo)
        pvk_b64 = base64.b64encode(pvk)
        assert (pvk, pbk) == pycspr.crypto.get_key_pair_from_base64(pvk_b64, key_algo)


def test_that_a_key_pair_can_be_deserialized_from_bytes(crypto_key_pair_specs):
    for key_algo, _, _ in crypto_key_pair_specs:
        pvk, pbk = pycspr.crypto.get_key_pair(key_algo)
        pvk_pem = pycspr.crypto.get_pvk_pem_from_bytes(pvk, key_algo)
        assert isinstance(pvk_pem, bytes)


def test_that_a_key_pair_can_be_deserialized_from_pem_file(crypto_key_pair_specs):
    for key_algo, _, _ in crypto_key_pair_specs:
        pvk, pbk = pycspr.crypto.get_key_pair(key_algo)
        path_to_pvk_pem_file = pycspr.crypto.get_pvk_pem_file_from_bytes(pvk, key_algo)
        assert pathlib.Path(path_to_pvk_pem_file).is_file()
        assert (pvk, pbk) == \
            pycspr.crypto.get_key_pair_from_pem_file(path_to_pvk_pem_file, key_algo)


def test_that_a_key_pair_can_be_deserialized_from_a_seed(crypto_key_pair_specs):
    for key_algo, pvk_length, pbk_length in crypto_key_pair_specs:
        seed = secrets.token_bytes(32)
        pvk, pbk = pycspr.crypto.get_key_pair_from_seed(seed, key_algo)
        assert len(pvk) == pvk_length
        assert len(pbk) == pbk_length


def test_that_a_public_key_is_deserializable_from_a_private_key_as_byte_array(crypto_key_pairs):
    for fixture in crypto_key_pairs:
        algo = pycspr.crypto.KeyAlgorithm[fixture["algo"]]
        _, pbk = pycspr.crypto.get_key_pair_from_bytes(fixture["pvk"], algo)
        assert fixture["pbk"] == pbk


def test_that_a_public_key_is_deserializable_from_a_private_key_as_base64(crypto_key_pairs):
    for fixture in crypto_key_pairs:
        algo = pycspr.crypto.KeyAlgorithm[fixture["algo"]]
        _, pbk = pycspr.crypto.get_key_pair_from_base64(base64.b64encode(fixture["pvk"]), algo)
        assert fixture["pbk"] == pbk


def test_that_a_public_key_is_deserializable_from_a_private_key_as_hex(crypto_key_pairs):
    for fixture in crypto_key_pairs:
        algo = pycspr.crypto.KeyAlgorithm[fixture["algo"]]
        _, pbk = pycspr.crypto.get_key_pair_from_hex_string(fixture["pvk"].hex(), algo)
        assert fixture["pbk"] == pbk


def test_that_a_signature_is_generatable(crypto_signatures):
    for fixture in crypto_signatures:
        algo = pycspr.crypto.KeyAlgorithm[fixture["key"]["algo"]]
        data = fixture["data"].encode("utf-8")
        pvk = fixture["key"]["pvk"]
        assert fixture["sig"] == \
            pycspr.crypto.get_signature(data, pvk, algo), \
            pycspr.crypto.get_signature(data, pvk, algo).hex()


def test_that_a_signature_is_verifiable(crypto_signatures):
    for fixture in crypto_signatures:
        algo = pycspr.crypto.KeyAlgorithm[fixture["key"]["algo"]]
        data = fixture["data"].encode("utf-8")
        sig = fixture["sig"]
        pbk = fixture["key"]["pbk"]
        assert pycspr.crypto.is_signature_valid(data, sig, pbk, algo)
