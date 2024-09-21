import typing

from pycspr.api.node.bin.codec import utils
from pycspr.api.node.bin.types.primitives import U8, U16, U32, U64


def decode_bytes(bytes_in: bytes) -> bytes:
    bytes_rem, length = utils.decode(bytes_in, U32)

    return bytes_rem


def decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


utils.register_decoder(bytes, decode_bytes)
utils.register_decoder(U8, lambda x: decode_uint(x, 1))
utils.register_decoder(U16, lambda x: decode_uint(x, 2))
utils.register_decoder(U32, lambda x: decode_uint(x, 4))
utils.register_decoder(U64, lambda x: decode_uint(x, 8))
