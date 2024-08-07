import typing

from pycspr.api.node.bin.codec.constants import \
    TAG_OPTIONAL_NONE, \
    TAG_OPTIONAL_VALUE

from pycspr.api.node.bin.types.primitives import U8x, U16x, U32x, U64x
from pycspr.api.node.bin.codec import utils

from pycspr.api.node.bin.codec.utils import \
    decode, \
    encode, \
    register_decoder, \
    register_encoder


register_decoder(U8x, lambda x: _decode_uint(x, 1))
register_decoder(U16x, lambda x: _decode_uint(x, 2))
register_decoder(U32x, lambda x: _decode_uint(x, 4))
register_decoder(U64x, lambda x: _decode_uint(x, 8))

register_encoder(bytes, lambda x: encode(len(x), U32x) + x)
register_encoder(U8x, lambda x: _encode_uint(x, 1))
register_encoder(U16x, lambda x: _encode_uint(x, 2))
register_encoder(U32x, lambda x: _encode_uint(x, 4))
register_encoder(U64x, lambda x: _encode_uint(x, 8))


def _decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def _encode_uint(entity: int, encoded_length: int) -> bytes:
    return entity.to_bytes(encoded_length, "little", signed=False)
