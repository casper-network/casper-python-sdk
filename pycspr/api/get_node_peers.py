from pycspr.api.constants import RPC_INFO_GET_STATUS
from pycspr.client import NodeConnectionInfo


def execute(node: NodeConnectionInfo) -> dict:
    """Returns node peers information.

    :param node: Information required to connect to a node.
    :returns: Node peers information.
    """
    response = node.get_response(RPC_INFO_GET_STATUS)
    return response["peers"]
