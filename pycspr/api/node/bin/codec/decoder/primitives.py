import typing


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
