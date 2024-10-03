import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.node import \
    NodeAddress, \
    NodeId, \
    NodePeerEntry, \
    NodeUptime
from pycspr.api.node.bin.types.primitives.numeric import U64


def decode_node_peer_entry(bytes_in: bytes) -> typing.Tuple[bytes, NodePeerEntry]:
    bytes_out, address = decode(NodeAddress, bytes_in)
    bytes_out, node_id = decode(NodeId, bytes_out)

    return bytes_out, NodePeerEntry(address, node_id)


register_decoders({
    (NodePeerEntry, decode_node_peer_entry),
    (NodeAddress, lambda x: decode(str, x)),
    (NodeId, lambda x: decode(str, x)),
    (NodeUptime, lambda x: decode(U64, x)),
})
