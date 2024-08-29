import typing

from pycspr.api.node.bin.codec import utils
from pycspr.api.node.bin.types.primitives import U8, U16, U32, U64


def _decode_bytes(bytes_in: bytes) -> typing.Tuple[bytes, bytes]:
    bytes_rem, length = utils.decode(bytes_in, U32)

    return bytes_rem


def _decode_uint(bytes_in: bytes, encoded_length: int) -> typing.Tuple[bytes, int]:
    return \
        bytes_in[encoded_length:], \
        int.from_bytes(bytes_in[:encoded_length], "little", signed=False)


def _encode_uint(entity: int, encoded_length: int) -> bytes:
    return entity.to_bytes(encoded_length, "little", signed=False)


utils.register_decoder(bytes, _decode_bytes)
utils.register_decoder(U8, lambda x: _decode_uint(x, 1))
utils.register_decoder(U16, lambda x: _decode_uint(x, 2))
utils.register_decoder(U32, lambda x: _decode_uint(x, 4))
utils.register_decoder(U64, lambda x: _decode_uint(x, 8))

utils.register_encoder(bytes, lambda x: utils.encode(len(x), U32) + x)
utils.register_encoder(U8, lambda x: _encode_uint(x, 1))
utils.register_encoder(U16, lambda x: _encode_uint(x, 2))
utils.register_encoder(U32, lambda x: _encode_uint(x, 4))
utils.register_encoder(U64, lambda x: _encode_uint(x, 8))
