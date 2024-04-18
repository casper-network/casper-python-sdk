import pycspr


def test_that_a_signature_is_generatable(crypto_signatures):
    for fixture in crypto_signatures:
        algo = pycspr.KeyAlgorithm[fixture["key"]["algo"]]
        data = fixture["data"].encode("utf-8")
        pvk = fixture["key"]["pvk"]
        assert fixture["sig"] == \
            pycspr.get_signature(data, algo, pvk), \
            pycspr.get_signature(data, algo, pvk).hex()


def test_that_a_signature_is_verifiable(crypto_signatures):
    for fixture in crypto_signatures:
        algo = pycspr.KeyAlgorithm[fixture["key"]["algo"]]
        data = fixture["data"].encode("utf-8")
        sig = fixture["sig"]
        pbk = fixture["key"]["pbk"]
        assert pycspr.is_signature_valid(data, algo, sig, pbk)
