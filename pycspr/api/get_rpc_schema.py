import pycspr
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(node: NodeConnectionInfo) -> dict:
    """Returns RPC schema.

    :param node: Information required to connect to a node.
    :returns: Node RPC API schema.

    """
    response = node.get_response(constants.RPC_DISCOVER)

    return response["schema"]
