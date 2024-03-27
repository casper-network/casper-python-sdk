import inspect

from pycspr.crypto import checksummer


def test_checksum_encoding(crypto_checksums):
    assert inspect.isfunction(checksummer.encode_bytes)
    for row in crypto_checksums:
        assert row["checksum"] == checksummer.encode_bytes(row["input"])


def test_checksum_decoding(crypto_checksums):
    assert inspect.isfunction(checksummer.decode_bytes)
    for row in crypto_checksums:
        encoded: str = checksummer.encode_bytes(row["input"])
        assert row["input"] == checksummer.decode_bytes(encoded)
