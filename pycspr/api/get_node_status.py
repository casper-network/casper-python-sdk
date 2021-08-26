import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns node status information.

    :param connection_info: Information required to connect to a node.
    :returns: Node status information.

    """
    response = rpc_client.request(
        connection_info.address_rpc,
        constants.RPC_INFO_GET_STATUS
        )

    return response.data.result
