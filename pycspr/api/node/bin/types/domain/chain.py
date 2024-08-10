import dataclasses
import typing

from pycspr.api.node.bin import utils
from pycspr.api.node.bin.types.crypto import DigestBytes
from pycspr.api.node.bin.types.primitives import U64


BlockHash = typing.NewType(
    "Digest over a block.", DigestBytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", U64
)

BlockID = typing.Union[BlockHash, BlockHeight]

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

TransactionHash = typing.NewType(
    "Digest over a transaction.", DigestBytes
    )

@dataclasses.dataclass
class BlockHeader():
    pass


@dataclasses.dataclass
class BlockRange():
    pass


@dataclasses.dataclass
class ProtocolVersion():
    """Version of protocol.

    """
    # Major semantic version.
    major: int

    # Minor semantic version.
    minor: int

    # Patch semantic version.
    patch: int

    @staticmethod
    def from_semvar(val: str):
        major, minor, patch = val.split(".")

        return ProtocolVersion(
            int(major),
            int(minor),
            int(patch)
        )
