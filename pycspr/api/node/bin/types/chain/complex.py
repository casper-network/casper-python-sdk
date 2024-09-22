import dataclasses
import typing

from pycspr.api.node.bin.types.primitives.crypto import DigestBytes
from pycspr.api.node.bin.types.primitives.numeric import U64


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

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
