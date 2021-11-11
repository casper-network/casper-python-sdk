from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import le_bytes_to_int


BYTE_LENGTH = 8


def from_bytes(value: bytes) -> int:
    return le_bytes_to_int(value, True)


def to_bytes(value: int) -> bytes:
    return int_to_le_bytes(value, BYTE_LENGTH, True)


def from_json(value: str) -> int:
    return int(value)


def to_json(value: int) -> str:
    return str(value)
