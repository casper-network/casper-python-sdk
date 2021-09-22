import dataclasses

from pycspr.utils.io import get_api_response



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


    def get_response(self, endpoint: str, params: dict = None) -> dict:
        """Invokes remote JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoints parameters.
        :returns: Parsed JSON-RPC response.
        
        """
        return get_api_response(self, endpoint, params)
