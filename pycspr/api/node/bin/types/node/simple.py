import typing

from pycspr.api.node.bin.types.primitives.numeric import U64
from pycspr.api.node.bin.types.primitives.time import Timestamp


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
