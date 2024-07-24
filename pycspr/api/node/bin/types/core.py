import dataclasses
import enum

from pycspr.api.node.bin.constants import DEFAULT_HOST
from pycspr.api.node.bin.constants import DEFAULT_PORT


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
    binary_request_version: int = 0

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
