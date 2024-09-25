import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.node import \
    NodeAddress, \
    NodeId, \
    NodePeerEntry, \
    NodeUptime
from pycspr.api.node.bin.types.primitives.numeric import U64


def decode_node_peer_entry(bytes_in: bytes) -> typing.Tuple[bytes, NodePeerEntry]:
    bytes_out, address = decode(bytes_in, NodeAddress)
    bytes_out, node_id = decode(bytes_out, NodeId)

    return bytes_out, NodePeerEntry(address, node_id)


register_decoders({
    (NodePeerEntry, decode_node_peer_entry),
    (NodeAddress, lambda x: decode(x, str)),
    (NodeId, lambda x: decode(x, str)),
    (NodeUptime, lambda x: decode(x, U64)),
})
