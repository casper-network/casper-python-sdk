import typing

from pycspr.api.node.bin.codec.chain.constants import \
    TAG_DOMAIN_BLOCK_HASH, \
    TAG_DOMAIN_BLOCK_HEIGHT
from pycspr.api.node.bin.codec.utils import encode, register_encoder
from pycspr.api.node.bin.types.domain import \
    BlockHash, \
    BlockHeader, \
    BlockHeight, \
    BlockID, \
    ProtocolVersion
from pycspr.api.node.bin.types.primitives import U8, U64


register_encoder(
    BlockHash,
    lambda x:
        encode(TAG_DOMAIN_BLOCK_HASH, U8) +
        encode(x, bytes)
    )

register_encoder(
    BlockHeight,
    lambda x:
        encode(TAG_DOMAIN_BLOCK_HEIGHT, U8) +
        encode(x, U64)
    )

register_encoder(
    BlockID,
    lambda x:
        encode(x, BlockHash) if isinstance(x, bytes) else
        encode(x, BlockHeight)
    )

register_encoder(
    ProtocolVersion,
    lambda x:
        encode(x.major, U8) +
        encode(x.minor, U8) +
        encode(x.patch, U8)
)
