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
