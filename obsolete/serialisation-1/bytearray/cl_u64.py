from pycspr.types import CLTypeKey
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import le_bytes_to_int
from pycspr.utils.constants import NUMERIC_CONSTRAINTS


# Range constraints.
_CONSTRAINTS = NUMERIC_CONSTRAINTS[CLTypeKey.U64]


def from_bytes(value: bytes) -> int:
    return le_bytes_to_int(value, False)


def from_json(value: str) -> int:
    return int(value)


def to_bytes(value: int) -> bytes:
    return int_to_le_bytes(value, _CONSTRAINTS.LENGTH, False)


def to_json(value: int) -> str:
    return str(value)
