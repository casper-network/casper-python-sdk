import dataclasses

from pycspr.api.node.rest.constants import DEFAULT_HOST
from pycspr.api.node.rest.constants import DEFAULT_PORT


@dataclasses.dataclass
class ConnectionInfo:
    """Encapsulates information required to connect to a node's REST API.

    """
    # Host address.
    host: str = DEFAULT_HOST

    # Number of exposed REST port.
    port: int = DEFAULT_PORT
