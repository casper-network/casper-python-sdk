import typing

from pycspr.api.node.bin.types.primitives import U64


NodeUptime = typing.NewType(
    "Number of milliseconds since a node has been up.", U64
)
