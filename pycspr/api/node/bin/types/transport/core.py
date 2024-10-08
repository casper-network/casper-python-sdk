from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.api.node.bin import constants
from pycspr.api.node.bin.types.chain import ProtocolVersion


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's BINARY API.

    """
    # Version of chain protocol, e..g. 2.0.0.
    chain_protocol_version: str

    # Host address.
    host: str = constants.DEFAULT_HOST

    # Host binary port.
    port: int = constants.DEFAULT_PORT

    # Version of binary server API.
    binary_request_version: int = constants.DEFAULT_REQUEST_VERSION

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


class ErrorCode(enum.Enum):
    """Enumeration over set of binary request error codes.

    """
    NoError = 0
    FunctionDisabled = 1
    NotFound = 2
    RootNotFound = 3
    InvalidItemVariant = 4
    WasmPreprocessing = 5
    UnsupportedProtocolVersion = 6
    InternalError = 7
    FailedQuery = 8
    BadRequest = 9
    UnsupportedRequest = 10
    DictionaryURefNotFound = 11
    NoCompleteBlocks = 12
    InvalidDeployChainName = 13
    InvalidDeployDependenciesNoLongerSupported = 14
    InvalidDeployExcessiveSize = 15
    InvalidDeployExcessiveTimeToLive = 16
    InvalidDeployTimestampInFuture = 17
    InvalidDeployBodyHash = 18
    InvalidDeployHash = 19
    InvalidDeployEmptyApprovals = 20
    InvalidDeployApproval = 21
    InvalidDeployExcessiveSessionArgsLength = 22
    InvalidDeployExcessivePaymentArgsLength = 23
    InvalidDeployMissingPaymentAmount = 24
    InvalidDeployFailedToParsePaymentAmount = 25
    InvalidDeployExceededBlockGasLimit = 26
    InvalidDeployMissingTransferAmount = 27
    InvalidDeployFailedToParseTransferAmount = 28
    InvalidDeployInsufficientTransferAmount = 29
    InvalidDeployExcessiveApprovals = 30
    InvalidDeployUnableToCalculateGasLimit = 31
    InvalidDeployUnableToCalculateGasCost = 32
    InvalidDeployUnspecified = 33
    InvalidTransactionChainName = 34
    InvalidTransactionExcessiveSize = 35
    InvalidTransactionExcessiveTimeToLive = 36
    InvalidTransactionTimestampInFuture = 37
    InvalidTransactionBodyHash = 38
    InvalidTransactionHash = 39
    InvalidTransactionEmptyApprovals = 40
    InvalidTransactionInvalidApproval = 41
    InvalidTransactionExcessiveArgsLength = 42
    InvalidTransactionExcessiveApprovals = 43
    InvalidTransactionExceedsBlockGasLimit = 44
    InvalidTransactionMissingArg = 45
    InvalidTransactionUnexpectedArgType = 46
    InvalidTransactionInvalidArg = 47
    InvalidTransactionInsufficientTransferAmount = 48
    InvalidTransactionEntryPointCannotBeCustom = 49
    InvalidTransactionEntryPointMustBeCustom = 50
    InvalidTransactionEmptyModuleBytes = 51
    InvalidTransactionGasPriceConversion = 52
    InvalidTransactionUnableToCalculateGasLimit = 53
    InvalidTransactionUnableToCalculateGasCost = 54
    InvalidTransactionPricingMode = 55
    InvalidTransactionUnspecified = 56
    InvalidTransactionOrDeployUnspecified = 57
    SwitchBlockNotFound = 58
    SwitchBlockParentNotFound = 59
    UnsupportedRewardsV1Request = 60
    BinaryProtocolVersionMismatch = 61


@dataclasses.dataclass
class Request():
    """Encapsulates information required to dispatch an API request.

    """
    # Request header encapsulating API metadata.
    header: "RequestHeader"

    # Request payload, i.e. endpoint params.
    payload: bytes = b''

    def __eq__(self, other: Request) -> bool:
        return self.header == other.header and self.payload == self.payload

    def __str__(self) -> str:
        return f"Request: {self.header} :: Payload Length={len(self.payload)}"


@dataclasses.dataclass
class RequestHeader():
    """Encapsulates API request header information.

    """
    # Version of binary server API.
    binary_request_version: int

    # Version of chain protocol.
    chain_protocol_version: ProtocolVersion

    # Request endpoint.
    endpoint: Endpoint

    # Request correlation identifier.
    id: int

    def __eq__(self, other: RequestHeader) -> bool:
        return \
            self.binary_request_version == other.binary_request_version and \
            self.chain_protocol_version == self.chain_protocol_version and \
            self.endpoint == other.endpoint and \
            self.id == other.id

    def __str__(self) -> str:
        return f"EndPoint={self.endpoint.name} | ID={self.id}"


RequestID = typing.NewType(
    "Request identifier specified by end user typically used to correlate responses.", int
)


@dataclasses.dataclass
class Response():
    """Response wrapper over raw bytes returned from server.

    """
    # Inner payload bytes.
    bytes_payload: bytes

    # Raw bytes.
    bytes_raw: bytes

    # Decoded header.
    header: ResponseHeader

    # Original request.
    request: Request

    # Inner payload.
    payload: typing.Union[object, typing.List[object]] = None

    def __str__(self) -> str:
        return f"Response: {self.header}"


@dataclasses.dataclass
class ResponseHeader():
    """Decoded response header.

    """
    # Chain protocol version.
    protocol_version: ProtocolVersion

    # Server error code.
    error_code: ErrorCode

    # Server data type.
    returned_data_type_tag: typing.Optional[int]

    def __str__(self) -> str:
        return "{} | Err={} | Data Type={}".format(
            self.protocol_version,
            self.error_code,
            self.returned_data_type_tag
        )
