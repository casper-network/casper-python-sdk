import dataclasses
import typing

from pycspr.api.node.bin import utils


BlockHash = typing.NewType(
    "Digest over a block.", bytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", int
)

BlockID = typing.Union[BlockHash, BlockHeight]

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

TransactionHash = typing.NewType(
    "Digest over a transaction.", bytes
    )

@dataclasses.dataclass
class BlockHeader():
    pass


@dataclasses.dataclass
class BlockRange():
    pass


@dataclasses.dataclass
class ProtocolVersion():
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

    # @staticmethod
    # def from_bytes(bytes_in: bytes) -> typing.Tuple[bytes, "ProtocolVersion"]:
    #     bytes_rem, major = U8.from_bytes(bytes_in)
    #     bytes_rem, minor = U8.from_bytes(bytes_rem)
    #     bytes_rem, patch = U8.from_bytes(bytes_rem)

    #     return bytes_rem, ProtocolVersion(major, minor, patch)
