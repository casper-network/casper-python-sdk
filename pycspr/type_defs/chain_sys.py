from __future__ import annotations

import dataclasses
import typing

from pycspr.type_defs.crypto import DigestBytes, PublicKey
from pycspr.type_defs.primitives import Timestamp


ChainNameDigest = typing.NewType(
    "Digest over a network's chain name.", DigestBytes
    )

Motes = typing.NewType(
    "Basic unit of crypto economic system.", int
    )

Weight = typing.NewType(
    "Some form of relative relevance measure.", int
    )


@dataclasses.dataclass
class ActivationPoint():
    """Point in time at which next chain upgrade activiation will occur.

    """
    pass


@dataclasses.dataclass
class ActivationPoint_Era(ActivationPoint):
    """Era at which upgrade activiation will occur.

    """
    # ID of era at which chain upgrade will occur.
    era_id: EraID


@dataclasses.dataclass
class ActivationPoint_Genesis(ActivationPoint):
    """Genesis timestamp at which upgrade activiation will occur.

    """
    # Timestamp upon which genesis started.
    timestamp: Timestamp


@dataclasses.dataclass
class ChainspecRawBytes():
    """Raw byte view over a chainspec.

    """
    # Raw bytes of the current chainspec.toml file.
    chainspec_bytes: bytes

    # Raw bytes of the current genesis accounts.toml file.
    maybe_genesis_accounts_bytes: typing.Optional[bytes]

    # Raw bytes of the current global_state.toml file.
    maybe_global_state_bytes: typing.Optional[bytes]


@dataclasses.dataclass
class NextUpgrade():
    """Future point in chain time when an upgrade will be applied.

    """
    # Activation point of the next upgrade.
    activation_point: ActivationPoint

    # Network protocol version at point when block was created.
    protocol_version: ProtocolVersion


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


ValidatorID = typing.NewType(
    "Validator identifier.", PublicKey
    )
