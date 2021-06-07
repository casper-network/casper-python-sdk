import dataclasses
import enum



@dataclasses.dataclass
class NodeConnectionInfo:
    """Encapsulates information required to connect to a node.
    
    """
    # Host address.
    host: str = "localhost"

    # Number of exposed REST port.
    port_rest: int = 50101

    # Number of exposed RPC port.
    port_rpc: int = 40101
    
    # Number of exposed SSE port.
    port_sse: int = 60101

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


@dataclasses.dataclass
class NodeDispatchInfo:
    """Encapsulates information required to dispatch to a node.
    
    """
    # Information required to connect to a node.
    connection: NodeConnectionInfo

    # Identifier of chain which dispatch is targetting.
    chain_id: str = "casper-net-1"

    # Maximum time interval before which dispatch processing will be cancelled.
    ttl: str = "1day"


class NodeEventType(enum.Enum):
    """Enumeration over set of exposed node event types.
    
    """
    API_VERSION = enum.auto()
    BLOCK_ADDED = enum.auto()
    BLOCK_FINALIZED = enum.auto()
    CONSENSUS_FINALITY_SIGNATURE = enum.auto()
    CONSENSUS_FAULT = enum.auto()
    DEPLOY_PROCESSED = enum.auto()


# Set of REST endpoints.
NODE_REST_ENDPOINTS: set = {
    "metrics",
    "status",
}

# Set of RPC endpoints.
NODE_RPC_ENDPOINTS: set = {
    "account_put_deploy",
    "info_get_deploy",
    "info_get_peers",
    "info_get_status",
    "chain_get_block",
    "chain_get_block_transfers",
    "chain_get_state_root_hash",
    "state_get_item",
    "state_get_balance",
    "chain_get_era_info_by_switch_block",
    "state_get_auction_info",
}

# Set of SSE endpoints.
NODE_SSE_ENDPOINTS: set = {
    "main",
    "sigs"
}
