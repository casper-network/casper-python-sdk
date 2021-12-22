import inspect

from pycspr.crypto import cl_checksum


def test_checksum_encoding(crypto_checksums):
    assert inspect.isfunction(cl_checksum.encode)
    for row in crypto_checksums:
        assert row["checksum"] == cl_checksum.encode(row["input"])


def test_checksum_decoding(crypto_checksums):
    assert inspect.isfunction(cl_checksum.decode)
    for row in crypto_checksums:
        encoded: str = cl_checksum.encode(row["input"])
        assert row["input"] == cl_checksum.decode(encoded)
