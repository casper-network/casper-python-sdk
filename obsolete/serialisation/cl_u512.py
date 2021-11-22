from pycspr.types import CLTypeKey
from pycspr.utils.conversion import int_to_le_bytes_trimmed
from pycspr.utils.conversion import le_bytes_to_int


BYTE_LENGTH = 64


def from_bytes(value: bytes) -> int:
    if value[0] <= BYTE_LENGTH:
        return le_bytes_to_int(value[1:], False)
    else:
        raise ValueError("Cannot decode U512 as bytes are too large")


def to_bytes(value: int) -> bytes:
    for type_key in (
        CLTypeKey.U8,
        CLTypeKey.U32,
        CLTypeKey.U64,
        CLTypeKey.U128,
        CLTypeKey.U256,
        CLTypeKey.U512
    ):
        if self.value >= constraints.MIN and self.value <= constraints.MAX:
            break
    else:
        raise ValueError("Invalid U512: max size exceeded")

    as_bytes = int_to_le_bytes_trimmed(value, BYTE_LENGTH, False)

    return bytes([len(as_bytes)]) + as_bytes


def from_json(value: str) -> int:
    return int(value)


def to_json(value: int) -> str:
    return str(value)
