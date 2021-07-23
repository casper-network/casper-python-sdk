import dataclasses
import enum



@dataclasses.dataclass
class NodeConnectionInfo:
    """Encapsulates information required to connect to a node.
    
    """
    # Host address.
    host: str = "localhost"

    # Number of exposed REST port.
    port_rest: int = 8888

    # Number of exposed RPC port.
    port_rpc: int = 7777
    
    # Number of exposed SSE port.
    port_sse: int = 9999

    @property
    def address(self) -> str:
        """A node's server base address."""
        return f"http://{self.host}"

    @property
    def address_rest(self) -> str:
        """A node's REST server base address."""
        return f"{self.address}:{self.port_rest}"

    @property
    def address_rpc(self) -> str:
        """A node's RPC server base address."""
        return f"{self.address}:{self.port_rpc}/rpc"

    @property
    def address_sse(self) -> str:
        """A node's SSE server base address."""
        return f"{self.address}:{self.port_sse}/events"

    def __str__(self):
        """Instance string representation."""
        return self.host


class NodeSseChannelType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    main = enum.auto()
    deploys = enum.auto()
    sigs = enum.auto()


class NodeSseEventType(enum.Enum):
    """Enumeration over set of exposed node SEE event types.
    
    """
    # All sub-channels.
    API_VERSION = enum.auto()

    # Main sub-channel.
    MAIN_BlockAdded = enum.auto()
    MAIN_DeployProcessed = enum.auto()
    MAIN_Fault = enum.auto()
    MAIN_Step = enum.auto()

    # Deploy sub-channel.
    DEPLOYS_DeployAccepted = enum.auto()

    # Sigs sub-channel.
    SIGNATURES_FinalitySignature = enum.auto()
