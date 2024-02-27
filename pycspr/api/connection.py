import dataclasses

from pycspr.api import constants


@dataclasses.dataclass
class NodeConnectionInfo:
    """Encapsulates information required to connect to a node.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed REST port.
    port_rest: int = constants.DEFAULT_PORT_REST

    # Number of exposed RPC port.
    port_rpc: int = constants.DEFAULT_PORT_RPC

    # Number of exposed speculative RPC port.
    port_rpc_speculative: int = constants.DEFAULT_PORT_SPECULATIVE_RPC

    # Number of exposed SSE port.
    port_sse: int = constants.DEFAULT_PORT_SSE

    def __str__(self):
        """Instance string representation."""
        return f"{self.host} :: REST @ {self.port_rest} :: RPC @ {self.port_rpc} :: RPC SPEC @ {self.port_rpc_speculative} :: SSE @ {self.port_sse}"
