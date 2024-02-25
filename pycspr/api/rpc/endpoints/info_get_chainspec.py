from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy


def exec(proxy: Proxy) -> dict:
    """Returns canonical network state information.

    :param proxy: Remote RPC server proxy.
    :returns: Chain spec, genesis accounts and global state information.

    """
    response: dict = proxy.get_response(constants.RPC_INFO_GET_CHAINSPEC)

    return response["chainspec_bytes"]
