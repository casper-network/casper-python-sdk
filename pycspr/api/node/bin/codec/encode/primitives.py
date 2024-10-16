from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.type_defs.primitives import U8, U16, U32, U64


def encode_uint(entity: int, encoded_length: int) -> bytes:
    return entity.to_bytes(encoded_length, "little", signed=False)


register_encoders({
    (bytes, lambda x: encode(len(x), U32) + x),
    (U8, lambda x: encode_uint(x, 1)),
    (U16, lambda x: encode_uint(x, 2)),
    (U32, lambda x: encode_uint(x, 4)),
    (U64, lambda x: encode_uint(x, 8)),
})
