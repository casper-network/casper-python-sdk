from pycspr.types import CLTypeKey
from pycspr.utils.constants import NUMERIC_CONSTRAINTS
from pycspr.utils.constants import is_within_range
from pycspr.utils.conversion import int_to_le_bytes_trimmed
from pycspr.utils.conversion import le_bytes_to_int


def from_bytes(value: bytes) -> int:
    if value[0] <= NUMERIC_CONSTRAINTS[CLTypeKey.U512].LENGTH:
        return le_bytes_to_int(value[1:], False)
    else:
        raise ValueError("Cannot decode U512 as bytes are too large")
    

def from_json(value: str) -> int:
    return int(value)


def to_bytes(value: int) -> bytes:
    for type_key in (
        CLTypeKey.U8,
        CLTypeKey.U32,
        CLTypeKey.U64,
        CLTypeKey.U128,
        CLTypeKey.U256,
        CLTypeKey.U512
    ):
        if is_within_range(type_key, value):
            break
    else:
        raise ValueError("Invalid U512: max size exceeded")

    constraints = NUMERIC_CONSTRAINTS[type_key]
    as_bytes = int_to_le_bytes_trimmed(value, constraints.LENGTH, False)

    return bytes([len(as_bytes)]) + as_bytes


def to_json(value: int) -> str:
    return str(value)
