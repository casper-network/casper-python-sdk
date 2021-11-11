from pycspr import crypto
from pycspr.types import PublicKey


def from_bytes(value: bytes) -> PublicKey:
    return PublicKey(
        crypto.KeyAlgorithm(value[0]),
        value[1:]
    )


def to_bytes(value: PublicKey) -> bytes:
    return bytes([value.algo.value]) + value.pbk


def from_json(value: str) -> PublicKey:
    return PublicKey(
        crypto.KeyAlgorithm(int(value[0:2])),
        bytes.fromhex(value[2:])
    )


def to_json(entity: PublicKey) -> str:
    return entity.account_key.hex()
