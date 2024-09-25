import typing

from pycspr.api.node.bin.types.primitives.numeric import U64


NodeAddress = typing.NewType(
    "Node host address.", str
)


NodeId = typing.NewType(
    "Canonical network wide node identifier.", str
)


NodeUptime = typing.NewType(
    "Number of milliseconds since a node has been up.", U64
)
