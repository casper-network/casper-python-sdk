import dataclasses
import typing

from pycspr.api.node.bin.types.domain.simple import \
    BlockID, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    PublicKey, \
    TransactionHash


@dataclasses.dataclass
class BlockHeader():
    pass


@dataclasses.dataclass
class BlockRange():
    pass


@dataclasses.dataclass
class NodeUptime():
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
