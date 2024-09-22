from pycspr.api.node.bin.codec.chain.constants import \
    TAG_DOMAIN_BLOCK_HASH, \
    TAG_DOMAIN_BLOCK_HEIGHT
from pycspr.api.node.bin.codec.utils import encode, register_encoders
from pycspr.api.node.bin.types.chain import \
    BlockHash, \
    BlockHeight, \
    BlockID, \
    ProtocolVersion
from pycspr.api.node.bin.types.primitives.numeric import U8, U64


def encode_block_hash(entity: BlockHash) -> bytes:
    return encode(TAG_DOMAIN_BLOCK_HASH, U8) + encode(entity, bytes)


def encode_block_height(entity: BlockHeight) -> bytes:
    return encode(TAG_DOMAIN_BLOCK_HEIGHT, U8) + encode(entity, U64)


def encode_block_id(entity: BlockID) -> bytes:
    encode_block_hash(entity) if isinstance(entity, bytes) else encode_block_height(entity)


def encode_protocol_version(entity: ProtocolVersion) -> bytes:
    return encode(entity.major, U8) + encode(entity.minor, U8) + encode(entity.patch, U8)


register_encoders({
    (BlockHash, encode_block_hash),
    (BlockHeight, encode_block_height),
    (BlockID, encode_block_id),
    (ProtocolVersion, encode_protocol_version),
})
