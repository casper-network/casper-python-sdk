import typing

from pycspr.api.node.bin.codec.utils import register_decoders
from pycspr.api.node.bin.codec import utils
from pycspr.api.node.bin.types.primitives import U8, U16, U32, U64


def decode_bytes(bytes_in: bytes) -> bytes:
    bytes_rem, length = utils.decode(bytes_in, U32)

    return bytes_rem


def decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


register_decoders({
    (bytes, decode_bytes),
    (U8, lambda x: decode_uint(x, 1)),
    (U16, lambda x: decode_uint(x, 2)),
    (U32, lambda x: decode_uint(x, 4)),
    (U64, lambda x: decode_uint(x, 8)),
})
