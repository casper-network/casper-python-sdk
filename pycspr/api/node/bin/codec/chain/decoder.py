import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.chain import BlockHeader, ProtocolVersion
from pycspr.api.node.bin.types.primitives.numeric import U32


def decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    print([int(i) for i in bytes_in], len(bytes_in))
    raise NotImplementedError()


def decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = decode(bytes_in, U32)
    bytes_rem, minor = decode(bytes_rem, U32)
    bytes_rem, patch = decode(bytes_rem, U32)

    return bytes_rem, ProtocolVersion(major, minor, patch)


register_decoders({
    (BlockHeader, decode_block_header),
    (ProtocolVersion, decode_protocol_version)
})
