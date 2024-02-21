import typing

from pycspr.api import constants
from pycspr.api.servers.rpc.utils import Proxy


def exec(proxy: Proxy) -> typing.List[dict]:
    """Returns node peer information.

    :param proxy: Remote RPC server proxy. 
    :returns: Node peer information.

    """
    response = proxy.get_response(constants.RPC_INFO_GET_PEERS)

    return response["peers"]
