import jsonrpcclient as rpc_client

import pycspr
from pycspr.types import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "rpc.discover"


def execute(
    connection_info: NodeConnectionInfo,
    parse_response: bool = True,
    ) -> dict:
    """Returns RPC schema.

    :param connection_info: Information required to connect to a node.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Node RPC API schema.

    """
    response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT)

    return response.data.result["schema"] if parse_response else response.data.result
