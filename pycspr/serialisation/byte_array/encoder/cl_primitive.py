import typing

from pycspr.types import CLTypeKey
from pycspr.utils.constants import NUMERIC_CONSTRAINTS
from pycspr.utils.constants import is_within_range
from pycspr.utils.conversion import int_to_le_bytes
from pycspr.utils.conversion import int_to_le_bytes_trimmed


def encode_any(value: object) -> bytes:
    """Encodes a value of an unassigned type.

    """
    raise NotImplementedError()


def encode_bool(value: bool) -> bytes:
    """Encodes a boolean.

    """
    return bytes([int(value)])


def encode_byte_array(value: bytes) -> bytes:
    """Encodes a byte array.

    """
    return bytes([]) if isinstance(value, type(None)) else value


def encode_i32(value: int) -> bytes:
    """Encodes a signed 32 bit integer.

    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.I32].LENGTH, True)


def encode_i64(value: int) -> bytes:
    """Encodes a signed 64 bit integer.

    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.I64].LENGTH, True)


def encode_string(value: str) -> bytes:
    """Encodes a string.

    """
    value = encode_byte_array((value or "").encode("utf-8"))

    return encode_u32(len(value)) + value


def encode_u8(value: int) -> bytes:
    """Encodes an unsigned 8 bit integer.

    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U8].LENGTH, False)


def encode_u8_array(value: typing.List[int]) -> bytes:
    """Encodes an array of unsigned 8 bit integers.

    """
    return encode_u32(len(value)) + bytes(value)


def encode_u32(value: int) -> bytes:
    """Encodes an unsigned 32 bit integer.

    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U32].LENGTH, False)


def encode_u64(value: int) -> bytes:
    """Encodes an unsigned 64 bit integer.

    """
    return int_to_le_bytes(value, NUMERIC_CONSTRAINTS[CLTypeKey.U64].LENGTH, False)


def encode_u128(value: int) -> bytes:
    """Encodes an unsigned 128 bit integer.

    """
    for type_key in (
        CLTypeKey.U8,
        CLTypeKey.U32,
        CLTypeKey.U64,
        CLTypeKey.U128
    ):
        if is_within_range(type_key, value):
            break
    else:
        raise ValueError("Invalid U128: max size exceeded")

    as_bytes = int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[type_key].LENGTH, False)

    return bytes([len(as_bytes)]) + as_bytes


def encode_u256(value: int) -> bytes:
    """Encodes an unsigned 256 bit integer.

    """
    for type_key in (
        CLTypeKey.U8,
        CLTypeKey.U32,
        CLTypeKey.U64,
        CLTypeKey.U128,
        CLTypeKey.U256
    ):
        if is_within_range(type_key, value):
            break
    else:
        raise ValueError("Invalid U256: max size exceeded")

    as_bytes = int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[type_key].LENGTH, False)

    return bytes([len(as_bytes)]) + as_bytes


def encode_u512(value: int):
    """Encodes an unsigned 512 bit integer.

    """
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

    as_bytes = int_to_le_bytes_trimmed(value, NUMERIC_CONSTRAINTS[type_key].LENGTH, False)

    return bytes([len(as_bytes)]) + as_bytes


def encode_unit(value: None):
    """Encodes a unitary CL value, i.e. a null.

    """
    return bytes([])
