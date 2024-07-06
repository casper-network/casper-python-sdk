import dataclasses
import typing


BlockHash = typing.NewType(
    "Digest over a block.", bytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", int
)

BlockID = typing.Union[BlockHash, BlockHeight]


@dataclasses.dataclass
class BlockHeader():
    pass


@dataclasses.dataclass
class ProtocolVersion():
    # Major semantic version.
    major: int
    # Minor semantic version.
    minor: int
    # Patch semantic version.
    patch: int
