import dataclasses

from pycspr.api.node.bin.types.node.simple import \
    NodeAddress, \
    NodeId


@dataclasses.dataclass
class NodePeerEntry():
    address: NodeAddress
    node_id: NodeId
