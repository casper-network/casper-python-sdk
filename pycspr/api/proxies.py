import dataclasses

import jsonrpcclient
import requests

from pycspr.api import constants


class NodeAPIError(Exception):
    """Node API error wrapper.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(NodeAPIError, self).__init__(msg)


@dataclasses.dataclass
class NodeRestServerProxy:
    """Node REST server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed REST port.
    port: int = constants.DEFAULT_PORT_REST

    @property
    def address(self) -> str:
        """A node's REST server base address."""
        return f"http://{self.host}:{self.port}"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def get_response(self, endpoint: str) -> dict:
        """Invokes remote REST API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :returns: Parsed REST API response.

        """
        return requests.get(f"{self.address}/{endpoint}").content.decode("utf-8")


@dataclasses.dataclass
class NodeRpcServerProxy:
    """Node JSON-RPC server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed REST port.
    port: int = constants.DEFAULT_PORT_RPC

    @property
    def address(self) -> str:
        """A node's RPC server base address."""
        return f"http://{self.host}:{self.port}/rpc"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def get_response(self, endpoint: str, params: dict = None) -> dict:
        """Invokes remote speculative JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoint parameters.
        :returns: Parsed JSON-RPC response.

        """
        response = requests.post(self.address, json=jsonrpcclient.request(endpoint, params))
        parsed = jsonrpcclient.parse(response.json())
        if isinstance(parsed, jsonrpcclient.responses.Error):
            raise NodeAPIError(parsed)

        return parsed.result
