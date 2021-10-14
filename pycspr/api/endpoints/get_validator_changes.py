from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection) -> dict:
    """Returns status changes of active validators.

    :param node: Information required to connect to a node.
    :returns: Status changes of active validators.

    """
    response = node.get_rpc_response(constants.RPC_INFO_GET_VALIDATOR_CHANGES)

    return response["changes"]
