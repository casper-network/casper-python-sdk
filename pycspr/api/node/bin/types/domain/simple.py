import typing


BlockHash = typing.NewType(
    "Digest over a block.", bytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", int
)

BlockID = typing.Union[BlockHash, BlockHeight]

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many era precede it.", int
)

PublicKey = typing.NewType(
    "Public key associated with an account.", bytes
    )

TransactionHash = typing.NewType(
    "Digest over a transaction.", bytes
    )
