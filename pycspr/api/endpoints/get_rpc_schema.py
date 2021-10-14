from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection) -> dict:
    """Returns RPC schema.

    :param node: Information required to connect to a node.
    :returns: Node RPC API schema.

    """
    response = node.get_rpc_response(constants.RPC_DISCOVER)

    return response["schema"]
