from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy


def exec(proxy: Proxy) -> dict:
    """Returns node status information.

    :param proxy: Remote RPC server proxy.
    :returns: Node status information.

    """
    return proxy.get_response(constants.RPC_INFO_GET_STATUS)
