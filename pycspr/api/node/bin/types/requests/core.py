from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.bin.types.domain import ProtocolVersion


@dataclasses.dataclass
class BaseRequest():
    """Base class encpasualting a request to be dispatched to remote binary port.

    """
    # Header encapsulates API metadata.
    header: "RequestHeader"


@dataclasses.dataclass
class Request():
    """Encapsulates information required to dispatch an API request.

    """
    # Request endpoint.
    endpoint: Endpoint

    # Request header encapsulating API metadata.
    header: "RequestHeader"

    # Request payload, i.e. endpoint params.
    payload: object = None


@dataclasses.dataclass
class RequestHeader():
    """Encapsulates API request header information.

    """
    # Version of binary server API.
    binary_request_version: int

    # Version of chain protocol.
    chain_protocol_version: ProtocolVersion

    # Request correlation identifier.
    id: "RequestID"


RequestID = typing.NewType(
    "Request identifier specified by end user typically used to correlate responses.", int
)


@dataclasses.dataclass
class RequestPayload():
    """Base class encpasualting payload of a request to be dispatched to remote binary port.

    """
    pass


class Endpoint(enum.Enum):
    """Enumeration over set of supported endpoints.

    """
    Get = 0
    Get_Information_AvailableBlockRange = 10
    Get_Information_BlockHeader = 0
    Get_Information_BlockSynchronizerStatus = 9
    Get_Information_ChainspecRawBytes = 13
    Get_Information_ConsensusStatus = 12
    Get_Information_ConsensusValidatorChanges = 8
    Get_Information_LastProgress = 5
    Get_Information_LatestSwitchBlockHeader = 15
    Get_Information_NetworkName = 7
    Get_Information_NextUpgrade = 11
    Get_Information_NodeStatus = 14
    Get_Information_Peers = 3
    Get_Information_ReactorState = 6
    Get_Information_Reward = 16
    Get_Information_SignedBlock = 1
    Get_Information_Transaction = 2
    Get_Information_Uptime = 4
    Try_AcceptTransaction = 1
    Try_SpeculativeExec = 2
