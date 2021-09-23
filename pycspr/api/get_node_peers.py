from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(node: NodeConnectionInfo) -> dict:
    """Returns node peers information.

    :param node: Information required to connect to a node.
    :returns: Node peers information.

    """
    response = node.get_response(constants.RPC_INFO_GET_STATUS)

    return response["peers"]
