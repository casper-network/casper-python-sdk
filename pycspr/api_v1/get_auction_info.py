import jsonrpcclient as rpc_client

from pycspr.client.connection_info import NodeConnectionInfo



# Method upon client to be invoked.
_API_ENDPOINT = "state_get_auction_info"


def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns current auction system contract information.

    :param connection_info: Information required to connect to a node.
    :returns: Current auction system contract information.

    """
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT)

    return response.data.result
