import typing

from pycspr.api.node.bin.codec.constants import \
    TYPE_TAG_PRIMITIVE_OPTIONAL_NONE, \
    TYPE_TAG_PRIMITIVE_OPTIONAL_VALUE


def encode_bytes(val: bytes) -> bytes:
    return encode_u32(len(val)) + val


def encode_optional(entity: object, encoder: typing.Callable) -> bytes:
    if entity is None:
        return encode_u8(TYPE_TAG_PRIMITIVE_OPTIONAL_NONE)
    else:
        return encode_u8(TYPE_TAG_PRIMITIVE_OPTIONAL_VALUE) + encoder(entity)


def encode_u8(val: int) -> bytes:
    return encode_uint(val, 1)


def encode_u16(val: int) -> bytes:
    return encode_uint(val, 2)


def encode_u32(val: int) -> bytes:
    return encode_uint(val, 4)


def encode_u64(val: int) -> bytes:
    return encode_uint(val, 8)


def encode_uint(val: int, encoded_length: int) -> bytes:
    return val.to_bytes(encoded_length, "little", signed=False)
