import dataclasses

from pycspr.api import constants


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's JSON-RPC API.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed RPC port.
    port: int = constants.DEFAULT_PORT_RPC
