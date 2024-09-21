from pycspr.api.node.bin.codec.utils import encode, register_encoder
from pycspr.api.node.bin.types.primitives import U8, U16, U32, U64


def encode_uint(entity: int, encoded_length: int) -> bytes:
    return entity.to_bytes(encoded_length, "little", signed=False)


register_encoder(bytes, lambda x: encode(len(x), U32) + x)
register_encoder(U8, lambda x: encode_uint(x, 1))
register_encoder(U16, lambda x: encode_uint(x, 2))
register_encoder(U32, lambda x: encode_uint(x, 4))
register_encoder(U64, lambda x: encode_uint(x, 8))
