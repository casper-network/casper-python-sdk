import dataclasses
import typing

import jsonrpcclient
import requests

from pycspr.api import constants
from pycspr.api.rpc.codec import decoder
from pycspr.api.rpc.utils import params as param_utils
from pycspr.types import BlockID


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

    def get_response(
        self,
        endpoint: str,
        params: dict = None,
        field: str = None,
    ) -> dict:
        """Invokes remote speculative JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoint parameters.
        :field: Inner response field.
        :returns: Parsed JSON-RPC response.

        """
        request = jsonrpcclient.request(endpoint, params)
        response_raw = requests.post(self.address, json=request)

        response_parsed = jsonrpcclient.parse(response_raw.json())
        if isinstance(response_parsed, jsonrpcclient.responses.Error):
            raise ProxyError(response_parsed)

        if field is None:
            return response_parsed.result
        else:
            return response_parsed.result[field]

    def chain_get_block_transfers(self, block_id: BlockID = None) -> dict:
        """Returns on-chain block transfers information.

        :param block_id: Identifier of a finalised block.
        :param decode: Flag indicating whether to decode API response.
        :returns: On-chain block transfers information.

        """    
        params: dict = param_utils.get_block_id(block_id, False)

        return self.get_response(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS, params)

class ProxyError(Exception):
    """Node API error wrapper.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(ProxyError, self).__init__(msg)
