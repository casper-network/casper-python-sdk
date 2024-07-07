import typing

from pycspr.api.node.bin.types.domain import \
    BlockID, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    PublicKey, \
    TransactionHash

from pycspr.api.node.bin.types.domain import \
    BlockHeader, \
    BlockRange, \
    NodeUptimeInfo, \
    ProtocolVersion


def _decode_block_header(bstream: bytes) -> typing.Tuple[bytes, BlockHeader]:
    raise NotImplementedError()
    return BlockHeader()


DECODERS: typing.Dict[typing.Type, typing.Callable] = {
    BlockHeader: _decode_block_header,
}
