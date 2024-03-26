import inspect

from pycspr import crypto


def test_checksum_encoding(crypto_checksums):
    assert inspect.isfunction(crypto.encode_bytes)
    for row in crypto_checksums:
        assert row["checksum"] == crypto.encode_bytes(row["input"])


def test_checksum_decoding(crypto_checksums):
    assert inspect.isfunction(crypto.decode_bytes)
    for row in crypto_checksums:
        encoded: str = crypto.encode_bytes(row["input"])
        assert row["input"] == crypto.decode_bytes(encoded)
