import dataclasses

import jsonrpcclient
import requests
import sseclient

from pycspr.api import constants
from pycspr.api.constants import NodeEventChannelType
from pycspr.utils.exceptions import NodeAPIError


@dataclasses.dataclass
class NodeConnection:
    """Encapsulates information required to connect to a node.

    """
    # Host address.
    host: str = "localhost"

    # Number of exposed REST port.
    port_rest: int = constants.DEFAULT_PORT_REST

    # Number of exposed RPC port.
    port_rpc: int = constants.DEFAULT_PORT_RPC

    # Number of exposed SSE port.
    port_sse: int = constants.DEFAULT_PORT_SSE

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


    def get_rest_response(self, endpoint: str) -> dict:
        """Invokes remote REST API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :returns: Parsed REST API response.

        """
        endpoint = f"{self.address_rest}/{endpoint}"
        response = requests.get(endpoint)

        return response.content.decode("utf-8")


    def get_rpc_response(self, endpoint: str, params: dict = None) -> dict:
        """Invokes remote JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoints parameters.
        :returns: Parsed JSON-RPC response.

        """
        response = requests.post(
            self.address_rpc,
            json=jsonrpcclient.request(endpoint, params),
            )

        parsed = jsonrpcclient.parse(response.json())
        if isinstance(parsed, jsonrpcclient.responses.Error):
            raise NodeAPIError(parsed)

        return parsed.result


    def get_sse_client(
        self,
        channel_type: NodeEventChannelType,
        event_id: int
    ) -> sseclient.SSEClient:
        """Returns SSE client.

        """
        url = f"{self.address_sse}/{channel_type.name.lower()}"
        if event_id:
            url = f"{url}?start_from={event_id}"
        stream = requests.get(url, stream=True)

        return sseclient.SSEClient(stream)
