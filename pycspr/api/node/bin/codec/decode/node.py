import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.type_defs.node import \
    NodeAddress, \
    NodeId, \
    NodeLastProgress, \
    NodePeerEntry, \
    NodeUptime
from pycspr.type_defs.primitives import U64, Timestamp


def _decode_node_peer_entry(bytes_in: bytes) -> typing.Tuple[bytes, NodePeerEntry]:
    rem, address = decode(NodeAddress, bytes_in)
    rem, node_id = decode(NodeId, rem)

    return rem, NodePeerEntry(address, node_id)


register_decoders({
    (NodePeerEntry, _decode_node_peer_entry),
    (NodeAddress, lambda x: decode(str, x)),
    (NodeId, lambda x: decode(str, x)),
    (NodeLastProgress, lambda x: decode(Timestamp, x)),
    (NodeUptime, lambda x: decode(U64, x)),
})
