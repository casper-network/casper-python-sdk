from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.bin.constants import \
    DEFAULT_HOST, \
    DEFAULT_PORT, \
    DEFAULT_REQUEST_VERSION
from pycspr.api.node.bin.types.domain import ProtocolVersion


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's BINARY API.

    """
    # Version of chain protocol, e..g. 2.0.0.
    chain_protocol_version: str

    # Host address.
    host: str = DEFAULT_HOST

    # Number of exposed speculative SSE port.
    port: int = DEFAULT_PORT

    # Version of binary server API.
    binary_request_version: int = DEFAULT_REQUEST_VERSION

    def get_url(self, eid: int = 0) -> str:
        """Returns URL for remote BIN server connection.

        """
        url: str = f"http://{self.host}:{self.port}/events"
        if eid:
            url = f"{url}?start_from={eid}"

        return url


class Endpoint(enum.Enum):
    """Enumeration over set of supported endpoints.

    """
    Get_Information_AvailableBlockRange = enum.auto()
    Get_Information_BlockHeader = enum.auto()
    Get_Information_BlockSynchronizerStatus = enum.auto()
    Get_Information_ChainspecRawBytes = enum.auto()
    Get_Information_ConsensusStatus = enum.auto()
    Get_Information_ConsensusValidatorChanges = enum.auto()
    Get_Information_LastProgress = enum.auto()
    Get_Information_LatestSwitchBlockHeader = enum.auto()
    Get_Information_NetworkName = enum.auto()
    Get_Information_NextUpgrade = enum.auto()
    Get_Information_NodeStatus = enum.auto()
    Get_Information_Peers = enum.auto()
    Get_Information_ReactorState = enum.auto()
    Get_Information_Reward = enum.auto()
    Get_Information_SignedBlock = enum.auto()
    Get_Information_Transaction = enum.auto()
    Get_Information_Uptime = enum.auto()
    Try_AcceptTransaction = enum.auto()
    Try_SpeculativeExec = enum.auto()


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

    def __eq__(self, other: Request) -> bool:
        return \
            self.endpoint == other.endpoint and \
            self.header == other.header and \
            self.payload == self.payload


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
class Response():
    """Response wrapper over raw bytes returned from server.

    """
    # Raw bytes.
    bytes_raw: bytes

    # Raw inner payload.
    bytes_payload: bytes

    # Decoded header.
    header: "ResponseHeader"

    # Original request.
    request: Request


@dataclasses.dataclass
class ResponseHeader():
    """Decoded response header.

    """
    # Chain protocol version.
    protocol_version: ProtocolVersion

    # Server error code.
    error: int

    # Server data type.
    returned_data_type_tag: typing.Optional[int]
