import typing

from pycspr.api.node.bin.codec.utils import decode
from pycspr.api.node.bin.codec.utils import encode
from pycspr.api.node.bin.codec.utils import register_decoder
from pycspr.api.node.bin.codec.utils import register_encoder
from pycspr.api.node.bin.codec import utils


from pycspr.api.node.bin.codec.constants import \
    TAG_DOMAIN_BLOCK_HASH, \
    TAG_DOMAIN_BLOCK_HEIGHT
from pycspr.api.node.bin.types.domain import \
    BlockHash, \
    BlockHeader, \
    BlockHeight, \
    BlockID, \
    EraID, \
    NodeUptime, \
    ProtocolVersion, \
    PublicKey, \
    TransactionHash
from pycspr.api.node.bin.types.primitives import \
    U8, \
    U64


def decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    raise NotImplementedError()


def decode_node_uptime(bytes_in: bytes) -> typing.Tuple[bytes, NodeUptime]:
    return decode(bytes_in, U64)


def decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = decode(bytes_in, U8)
    bytes_rem, minor = decode(bytes_rem, U8)
    bytes_rem, patch = decode(bytes_rem, U8)

    return bytes_rem, ProtocolVersion(major, minor, patch)


utils.register_decoder(BlockHeader, decode_block_header)
utils.register_decoder(NodeUptime, decode_node_uptime)
utils.register_decoder(ProtocolVersion, decode_protocol_version)

utils.register_encoder(BlockHash, lambda x:
    encode(TAG_DOMAIN_BLOCK_HASH, U8) + encode(x, bytes)
)

utils.register_encoder(BlockHeight, lambda x:
    encode(TAG_DOMAIN_BLOCK_HEIGHT, U8) + encode(x, U64)
)

utils.register_encoder(BlockID, lambda x:
    encode(x, BlockHash) if isinstance(x, bytes) else
    encode(x, BlockHeight)
)

utils.register_encoder(ProtocolVersion, lambda x:
    encode(x.major, U8) +
    encode(x.minor, U8) +
    encode(x.patch, U8)
)
