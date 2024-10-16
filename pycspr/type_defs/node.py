import dataclasses
import typing

from pycspr.type_defs.primitives import U64, Timestamp


NodeAddress = typing.NewType(
    "Node host address.", str
)

NodeId = typing.NewType(
    "Canonical network wide node identifier.", str
)

NodeLastProgress = typing.NewType(
    "Timestamp tracking node's linear chain progression.", Timestamp
)

NodeUptime = typing.NewType(
    "Number of milliseconds since a node has been up.", U64
)

@dataclasses.dataclass
class NodePeerEntry():
    address: NodeAddress
    node_id: NodeId
