import jsonrpcclient as rpc_client

import pycspr
from pycspr.client import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "rpc.discover"


def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns RPC schema.

    :param connection_info: Information required to connect to a node.
    :returns: Node RPC API schema.

    """
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT)

    return response.data.result["schema"]
