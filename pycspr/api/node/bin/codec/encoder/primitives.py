import typing


def encode_bytes(val: bytes):
    return encode_u32(len(val)) + val


def encode_optional(val: object, encoder: typing.Callable):
    if val is None:
        return encode_u8(0)
    else:
        return encode_u8(1) + encoder(val)


def encode_u8(val: int):
    return encode_uint(val, 1)


def encode_u16(val: int):
    return encode_uint(val, 2)


def encode_u32(val: int):
    return encode_uint(val, 4)


def encode_u64(val: int):
    return encode_uint(val, 8)


def encode_uint(val: int, encoded_length: int):
    return val.to_bytes(encoded_length, "little", signed=False)
