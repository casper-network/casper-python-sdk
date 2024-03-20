import dataclasses

from pycspr.api import constants


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's SSE API.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed speculative SSE port.
    port: int = constants.DEFAULT_PORT_SSE

    # Number of exposed JSON-RPC port.
    port_rpc: int = constants.DEFAULT_PORT_RPC
