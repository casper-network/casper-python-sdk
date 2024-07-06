def decode(bstream: bytes) -> object:
    return bstream


def decode_u8(val: bytes):
    return decode_uint(val, 1)


def decode_u16(val: bytes):
    return decode_uint(val, 2)


def decode_u32(val: bytes):
    return decode_uint(val, 4)


def decode_u64(val: bytes):
    return decode_uint(val, 8)


def decode_uint(val: bytes, encoded_length: int):
    return int.from_bytes(val, "little", signed=False)
