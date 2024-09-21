import dataclasses

from pycspr.api import constants


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's speculative JSON-RPC API.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed speculative RPC port.
    port: int = constants.DEFAULT_PORT_SPECULATIVE_RPC
