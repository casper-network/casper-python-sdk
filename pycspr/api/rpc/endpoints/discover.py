from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy


def exec(proxy: Proxy) -> dict:
    """Returns RPC schema.

    :param proxy: Remote RPC server proxy.
    :returns: Node JSON-RPC API schema.

    """
    response: dict = proxy.get_response(constants.RPC_DISCOVER)

    return response["schema"]
