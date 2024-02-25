import typing

from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy


def exec(proxy: Proxy) -> typing.List[dict]:
    """Returns node peer information.

    :param proxy: Remote RPC server proxy.
    :returns: Node peer information.

    """
    response: dict = proxy.get_response(constants.RPC_INFO_GET_PEERS)

    return response["peers"]
