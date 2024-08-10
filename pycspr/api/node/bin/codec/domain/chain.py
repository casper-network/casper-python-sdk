import typing

from pycspr.api.node.bin.codec import utils


from pycspr.api.node.bin.codec.constants import \
    TAG_DOMAIN_BLOCK_HASH, \
    TAG_DOMAIN_BLOCK_HEIGHT
from pycspr.api.node.bin.types.domain import \
    BlockHash, \
    BlockHeader, \
    BlockHeight, \
    BlockID, \
    ProtocolVersion
from pycspr.api.node.bin.types.primitives import \
    U8, \
    U64


def _decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    raise NotImplementedError()


def _decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = utils.decode(bytes_in, U8)
    bytes_rem, minor = utils.decode(bytes_rem, U8)
    bytes_rem, patch = utils.decode(bytes_rem, U8)

    return bytes_rem, ProtocolVersion(major, minor, patch)


utils.register_decoder(BlockHeader, _decode_block_header)
utils.register_decoder(ProtocolVersion, _decode_protocol_version)

utils.register_encoder(
    BlockHash,
    lambda x:
        utils.encode(TAG_DOMAIN_BLOCK_HASH, U8) +
        utils.encode(x, bytes)
    )

utils.register_encoder(
    BlockHeight,
    lambda x:
        utils.encode(TAG_DOMAIN_BLOCK_HEIGHT, U8) +
        utils.encode(x, U64)
    )

utils.register_encoder(
    BlockID,
    lambda x:
        utils.encode(x, BlockHash) if isinstance(x, bytes) else
        utils.encode(x, BlockHeight)
    )

utils.register_encoder(
    ProtocolVersion,
    lambda x:
        utils.encode(x.major, U8) +
        utils.encode(x.minor, U8) +
        utils.encode(x.patch, U8)
)
