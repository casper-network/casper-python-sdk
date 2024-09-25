import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.primitives.numeric import U8, U16, U32, U64


def decode_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    bytes_rem, length = decode(bytes_in, U32)

    return bytes_rem


def decode_str(bytes_in: bytes) -> typing.Tuple[bytes, str]:
    bytes_out, size = decode(bytes_in, U32)
    assert len(bytes_out) >= size

    return bytes_out[size:], bytes_out[0:size].decode("utf-8")


def decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


register_decoders({
    (bytes, decode_bytes),
    (str, decode_str),
    (U8, lambda x: decode_uint(x, 1)),
    (U16, lambda x: decode_uint(x, 2)),
    (U32, lambda x: decode_uint(x, 4)),
    (U64, lambda x: decode_uint(x, 8)),
})
