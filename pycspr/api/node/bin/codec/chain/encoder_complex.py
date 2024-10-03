from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.api.node.bin.types.chain import ProtocolVersion
from pycspr.api.node.bin.types.primitives.numeric import U8


def encode_protocol_version(entity: ProtocolVersion) -> bytes:
    return encode(entity.major, U8) + encode(entity.minor, U8) + encode(entity.patch, U8)


register_encoders({
    (ProtocolVersion, encode_protocol_version),
})
