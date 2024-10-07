import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.types.node import \
    NodeAddress, \
    NodeId, \
    NodeLastProgress, \
    NodePeerEntry, \
    NodeUptime
from pycspr.api.node.bin.types.primitives.numeric import U64
from pycspr.api.node.bin.types.primitives.time import Timestamp


def _decode_node_peer_entry(bytes_in: bytes) -> typing.Tuple[bytes, NodePeerEntry]:
    bytes_rem, address = decode(NodeAddress, bytes_in)
    bytes_rem, node_id = decode(NodeId, bytes_rem)

    return bytes_rem, NodePeerEntry(address, node_id)


register_decoders({
    (NodePeerEntry, _decode_node_peer_entry),
    (NodeAddress, lambda x: decode(str, x)),
    (NodeId, lambda x: decode(str, x)),
    (NodeLastProgress, lambda x: decode(Timestamp, x)),
    (NodeUptime, lambda x: decode(U64, x)),
})
