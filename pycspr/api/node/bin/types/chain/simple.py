import dataclasses
import typing

from pycspr.api.node.bin.types.primitives.crypto import DigestBytes
from pycspr.api.node.bin.types.primitives.numeric import U64


BlockHash = typing.NewType(
    "Digest over a block.", DigestBytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", U64
)

BlockBodyHash = typing.NewType(
    "Digest over a block's body.", DigestBytes
    )

BlockID = typing.Union[BlockHash, BlockHeight]

GasPrice = typing.NewType(
    "Multiplier applied to estimation of computational costs (gas).", int
)

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

TransactionHash = typing.NewType(
    "Digest over a transaction.", DigestBytes
    )
