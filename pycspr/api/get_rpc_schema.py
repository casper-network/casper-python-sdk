from jsonrpcclient import parse, request
import requests

import pycspr
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(node: NodeConnectionInfo) -> dict:
    """Returns RPC schema.

    :param node: Information required to connect to a node.
    :returns: Node RPC API schema.

    """
    response = requests.post(
        node.address_rpc,
        json=request(constants.RPC_DISCOVER)
        )

    return parse(response.json()).result["schema"]
