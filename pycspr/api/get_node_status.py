from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(node: NodeConnectionInfo) -> dict:
    """Returns node status information.

    :param node: Information required to connect to a node.
    :returns: Node status information.

    """
    return node.get_response(constants.RPC_INFO_GET_STATUS)
