import typing

from pycspr.api.node.bin.codec.constants import \
    TAG_OPTIONAL_NONE, \
    TAG_OPTIONAL_VALUE


def decode_u8(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 1)


def decode_u16(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 2)


def decode_u32(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 4)


def decode_u64(bstream: bytes) -> typing.Tuple[bytes, int]:
    return decode_uint(bstream, 8)


def decode_uint(bstream: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bstream[encoded_length:], \
        int.from_bytes(bstream[:encoded_length], "little", signed=False)


def encode_bytes(val: bytes) -> bytes:
    return encode_u32(len(val)) + val


def encode_optional(entity: object, encoder: typing.Callable) -> bytes:
    if entity is None:
        return encode_u8(TAG_OPTIONAL_NONE)
    else:
        return encode_u8(TAG_OPTIONAL_VALUE) + encoder(entity)


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
