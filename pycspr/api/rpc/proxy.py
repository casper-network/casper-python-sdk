import dataclasses

import jsonrpcclient
import requests

from pycspr.api import constants


@dataclasses.dataclass
class Proxy:
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
        request = jsonrpcclient.request(endpoint, params)
        response = requests.post(self.address, json=request)
        response_parsed = jsonrpcclient.parse(response.json())
        if isinstance(response_parsed, jsonrpcclient.responses.Error):
            raise ProxyError(response_parsed)

        return response_parsed.result


class ProxyError(Exception):
    """Node API error wrapper.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(ProxyError, self).__init__(msg)
