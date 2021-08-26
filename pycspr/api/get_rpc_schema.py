import jsonrpcclient as rpc_client

import pycspr
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns RPC schema.

    :param connection_info: Information required to connect to a node.
    :returns: Node RPC API schema.

    """
    response = rpc_client.request(
        connection_info.address_rpc,
        constants.RPC_DISCOVER
        )

    return response.data.result["schema"]
