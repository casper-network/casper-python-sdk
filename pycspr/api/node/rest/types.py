from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.types.crypto import DigestBytes
from pycspr.types.crypto import PublicKey


BlockHash = typing.NewType(
    "Digest over a block.", DigestBytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", int
)

EraID = typing.NewType(
    "Identifier of an era in chain time.", int
    )

StateRootHash = typing.NewType(
    "Root digest of a node's global state.", DigestBytes
    )


class ReactorState(enum.Enum):
    INITIALIZE = "Initialize"
    CATCH_UP = "CatchUp"
    UPGRADING = "Upgrading"
    KEEP_UP = "KeepUp"
    VALIDATE = "Validate"
    SHUTDOWN_FOR_UPGRADE = "ShutdownForUpgrade"


class ValidatorStatusChangeType(enum.Enum):
    ADDED = "Added"
    REMOVED = "Removed"
    BANNED = "Banned"
    CANNOT_PROPOSE = "CannotPropose"
    SEEN_AS_FAULTY = "SeenAsFaulty"


@dataclasses.dataclass
class BlockRange():
    low: int
    high: int


@dataclasses.dataclass
class MinimalBlockInfo():
    creator: PublicKey
    era_id: EraID
    hash: BlockHash
    height: BlockHeight
    state_root_hash: StateRootHash
    timestamp: Timestamp


@dataclasses.dataclass
class NextUpgradeInfo():
    activation_point: str
    protocol_version: str


@dataclasses.dataclass
class NodePeer():
    address: str
    node_id: str


@dataclasses.dataclass
class NodeStatus():
    api_version: str
    available_block_range: BlockRange
    build_version: str
    chainspec_name: str
    last_added_block_info: MinimalBlockInfo
    last_progress: Timestamp
    next_upgrade: NextUpgradeInfo
    our_public_signing_key: PublicKey
    peers: typing.List[NodePeer]
    reactor_state: ReactorState
    round_length: str
    starting_state_root_hash: StateRootHash
    uptime: str


@dataclasses.dataclass
class Timestamp():
    value: float


@dataclasses.dataclass
class ValidatorChanges():
    public_key: PublicKey
    status_changes: typing.List[ValidatorStatusChange]
