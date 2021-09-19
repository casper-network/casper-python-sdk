from jsonrpcclient import parse, request
import requests

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(connection_info: NodeConnectionInfo) -> dict:
    """Returns node status information.

    :param connection_info: Information required to connect to a node.
    :returns: Node status information.

    """
    response = requests.post(
        connection_info.address_rpc,
        json=request(constants.RPC_INFO_GET_STATUS)
        )

    return parse(response.json()).result
