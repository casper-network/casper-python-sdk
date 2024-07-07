from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.bin.types.domain import ProtocolVersion


@dataclasses.dataclass
class Request():
    # Body encapsulates endpoint plus payload.
    body: object

    # Header encapsulates API metadata.
    header: "RequestHeader"


@dataclasses.dataclass
class RequestHeader():
    # Version of binary server API.
    binary_request_version: int

    # Version of chain protocol.
    chain_protocol_version: ProtocolVersion

    # Request type tag.
    type_tag: "RequestType"

    # Request correlation identifier.
    id: int


RequestID = typing.NewType(
    "Request identifier specified by end user typically used to correlate responses.", int
)


class RequestType(enum.Enum):
    Get = 0
    TryAcceptTransaction = 1
    TrySpeculativeExec = 2


class RequestType_Get(enum.Enum):
    Information = 1
    Record = 0
    State = 2


class RequestType_Get_Information(enum.Enum):
    AvailableBlockRange = 10
    BlockHeader = 0
    BlockSynchronizerStatus = 9
    ChainspecRawBytes = 13
    ConsensusStatus = 12
    ConsensusValidatorChanges = 8
    LastProgress = 5
    LatestSwitchBlockHeader = 15
    NetworkName = 7
    NextUpgrade = 11
    NodeStatus = 14
    Peers = 3
    ReactorState = 6
    Reward = 16
    SignedBlock = 1
    Transaction = 2
    Uptime = 4
