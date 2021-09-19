from jsonrpcclient import parse, request
import requests

import pycspr
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns RPC schema.

    :param connection_info: Information required to connect to a node.
    :returns: Node RPC API schema.

    """
    response = requests.post(
        connection_info.address_rpc,
        json=request(constants.RPC_DISCOVER)
        )

    return parse(response.json()).result["schema"]
