import operator

import pycspr


def test_get_hash(crypto_hashes):
    getter_1 = operator.itemgetter("data", "hashes")
    getter_2 = operator.itemgetter("algo", "digest")
    for data, hashes in [getter_1(i) for i in crypto_hashes]:
        for algo, digest in [getter_2(j) for j in hashes]:
            algo = pycspr.HashAlgorithm[algo]
            assert digest == pycspr.get_hash(data.encode("utf-8"), 32, algo)


def test_get_account(crypto_key_pairs):
    getter = operator.itemgetter("algo", "pbk", "accountKey", "accountHash")
    for algo, pbk, account_key, accountHash in [getter(i) for i in crypto_key_pairs]:
        algo = pycspr.KeyAlgorithm[algo]
        assert account_key == pycspr.get_account_key(algo, pbk)
        print(pycspr.get_account_hash(account_key).hex())
        assert pycspr.get_account_hash(account_key) == accountHash
