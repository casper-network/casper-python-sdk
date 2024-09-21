import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoder
from pycspr.api.node.bin.types.domain import \
    BlockHeader, \
    ProtocolVersion
from pycspr.api.node.bin.types.primitives import U8, U32


def decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    raise NotImplementedError()


def decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = decode(bytes_in, U32)
    bytes_rem, minor = decode(bytes_rem, U32)
    bytes_rem, patch = decode(bytes_rem, U32)

    return bytes_rem, ProtocolVersion(major, minor, patch)


register_decoder(BlockHeader, decode_block_header)
register_decoder(ProtocolVersion, decode_protocol_version)
