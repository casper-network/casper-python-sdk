import jsonrpcclient as rpc_client
import requests

from pycspr.client import NodeConnectionInfo


# Method upon client to be invoked.
_API_ENDPOINT = "info_get_peers"


def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns node peers information.

    :param connection_info: Information required to connect to a node.
    :returns: Node peers information.

    """
    response = requests.post(
        connection_info.address_rpc,
        json=request(_API_ENDPOINT))

    parsed = parse(response.json())

    return parsed.result["peers"]
