import typing

from pycspr.api.node.bin.codec.constants import \
    TAG_OPTIONAL_NONE, \
    TAG_OPTIONAL_VALUE


def decode_u8(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 1)


def decode_u16(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 2)


def decode_u32(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 4)


def decode_u64(bytes_in: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bytes_in, 8)


def decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def encode_bytes(entity: bytes) -> bytes:
    return encode_u32(len(entity)) + entity


def encode_optional(entity: object, encoder: typing.Callable) -> bytes:
    if entity is None:
        return encode_u8(TAG_OPTIONAL_NONE)
    else:
        return encode_u8(TAG_OPTIONAL_VALUE) + encoder(entity)


def encode_u8(entity: int) -> bytes:
    return encode_uint(entity, 1)


def encode_u16(entity: int) -> bytes:
    return encode_uint(entity, 2)


def encode_u32(entity: int) -> bytes:
    return encode_uint(entity, 4)


def encode_u64(entity: int) -> bytes:
    return encode_uint(entity, 8)


def encode_uint(entity: int, encoded_length: int) -> bytes:
    return entity.to_bytes(encoded_length, "little", signed=False)
