from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection) -> dict:
    """Returns node peers information.

    :param node: Information required to connect to a node.
    :returns: Node peers information.

    """
    response = node.get_rpc_response(constants.RPC_INFO_GET_STATUS)

    return response["peers"]
