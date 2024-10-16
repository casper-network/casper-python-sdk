from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.type_defs.crypto import DigestBytes, PublicKey
from pycspr.type_defs.chain import \
    AvailableBlockRange as BlockRange, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    StateRootHash
from pycspr.type_defs.node import ReactorState
from pycspr.type_defs.primitives import Timestamp


class ValidatorStatusChangeType(enum.Enum):
    ADDED = "Added"
    REMOVED = "Removed"
    BANNED = "Banned"
    CANNOT_PROPOSE = "CannotPropose"
    SEEN_AS_FAULTY = "SeenAsFaulty"


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
    # block_sync: TODO
    build_version: str
    chainspec_name: str
    last_added_block_info: MinimalBlockInfo
    latest_switch_block_hash: BlockHash
    last_progress: Timestamp
    next_upgrade: NextUpgradeInfo
    our_public_signing_key: PublicKey
    peers: typing.List[NodePeer]
    reactor_state: ReactorState
    round_length: str
    starting_state_root_hash: StateRootHash
    uptime: str


@dataclasses.dataclass
class ValidatorChanges():
    public_key: PublicKey
    status_changes: typing.List[ValidatorStatusChange]
