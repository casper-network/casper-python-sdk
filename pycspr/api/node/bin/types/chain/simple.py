import typing

from pycspr.api.node.bin.types.crypto import DigestBytes
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

DelegationRate = typing.NewType(
    "Delegation rate of tokens. Range from 0..=100.", int
    )

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

GasPrice = typing.NewType(
    "Multiplier applied to estimation of computational costs (gas).", int
)

Motes = typing.NewType(
    "Basic unit of crypto economic system.", int
    )

TransactionHash = typing.NewType(
    "Digest over a transaction.", DigestBytes
    )

Weight = typing.NewType(
    "Some form of relative relevance measure.", int
    )
