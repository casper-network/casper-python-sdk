from __future__ import annotations

import dataclasses
import typing

from pycspr.api.node.bin.types.chain.simple import \
    BlockHash, \
    BlockHeight, \
    EraID
from pycspr.api.node.bin.types.primitives.crypto import DigestBytes, PublicKeyBytes
from pycspr.api.node.bin.types.primitives.numeric import U64
from pycspr.api.node.bin.types.primitives.time import Timestamp



@dataclasses.dataclass
class Block():
    """A block after execution, with the resulting global state root hash.

    """
    # Body of block.
    # body: typing.Union["BlockBody_V1", "BlockBody_V2"]

    # Digest over block.
    hash: "BlockHash"

    # Header of block.
    header: typing.Union["BlockHeader_V1", "BlockHeader_V2"]


@dataclasses.dataclass
class BlockHeader():
    """Block header encpasulating versioned header portion of a block.

    """
    pass


@dataclasses.dataclass
class BlockHeader_V1(BlockHeader):
    """Block header encpasulating version 1 header portion of a block.

    """
    # Future era initializion seed.
    accumulated_seed: DigestBytes

    # Digest over block body.
    body_hash: DigestBytes

    # Digest over block body.
    era_end: typing.Optional["EraEnd_V1"]

    # Height of era, i.e. number of ancestors.
    era_id: "EraID"

    # Height of block, i.e. number of ancestors.
    height: "BlockHeight"

    # Digest over parent block.
    parent_hash: "BlockHash"

    # Future era initializion random bit.
    random_bit: bool

    # Network protocol version at point when block was created.
    protocol_version: "ProtocolVersion"

    # Digest over post block execution state root.
    state_root_hash: DigestBytes

    # Timestamp from when the block was proposed.
    timestamp: bytes


@dataclasses.dataclass
class BlockHeader_V2(BlockHeader):
    """Block header encpasulating version 2 header portion of a block.

    """
    # A seed needed for initializing a future era.
    accumulated_seed: DigestBytes

    # The hash of the block's body.
    body_hash: DigestBytes

    # The gas price of the era
    current_gas_price: int

    # The `EraEnd` of a block if it is a switch block.
    era_end: typing.Optional[EraEnd_V2]

    # The era ID in which this block was created.
    era_id: EraID

    # The height of this block, i.e. the number of ancestors.
    height: int

    # The most recent switch block hash.
    last_switch_block_hash: typing.Optional[BlockHash]

    # The parent block's hash.
    parent_hash: BlockHash

    # The public key of the validator which proposed the block.
    proposer: PublicKeyBytes

    # The protocol version of the network from when this block was created.
    protocol_version: ProtocolVersion

    # A random bit needed for initializing a future era.
    random_bit: bool

    # The root hash of global state after the deploys in this block have been executed.
    state_root_hash: DigestBytes

    # The timestamp from when the block was proposed.
    timestamp: Timestamp


@dataclasses.dataclass
class EraEnd_V1():
    """End of era information scoped by block header version 1.

    """
    pass


@dataclasses.dataclass
class EraEnd_V2():
    """End of era information scoped by block header version 2.

    """
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

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"
