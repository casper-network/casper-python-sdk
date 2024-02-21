from pycspr.api import constants
from pycspr.api.servers.rpc.utils import Proxy


def exec(proxy: Proxy) -> dict:
    """Returns RPC schema.

    :param proxy: Remote RPC server proxy. 
    :returns: Node JSON-RPC API schema.

    """
    response = proxy.get_response(constants.RPC_DISCOVER)

    return response["schema"]
