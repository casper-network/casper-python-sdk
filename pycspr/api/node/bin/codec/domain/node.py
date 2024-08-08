import typing

from pycspr.api.node.bin.codec import utils
from pycspr.api.node.bin.types.domain import NodeUptime
from pycspr.api.node.bin.types.primitives import U64


def _decode_node_uptime(bytes_in: bytes) -> typing.Tuple[bytes, NodeUptime]:
    return utils.decode(bytes_in, U64)


utils.register_decoder(NodeUptime, _decode_node_uptime)
