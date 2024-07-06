import dataclasses

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
