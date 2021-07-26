import jsonrpcclient as rpc_client

from pycspr.client import NodeConnectionInfo



# Method upon client to be invoked.
_API_ENDPOINT = "info_get_status"


def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns node status information.

    :param connection_info: Information required to connect to a node.
    :returns: Node status information.

    """
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT)

    return response.data.result
