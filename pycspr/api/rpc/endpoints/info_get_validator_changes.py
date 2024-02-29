import typing

from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy


def exec(proxy: Proxy) -> typing.List[dict]:
    """Returns validator change set.

    :param proxy: Remote RPC server proxy.
    :returns: Validator change set.

    """
    return proxy.get_response(constants.RPC_INFO_GET_VALIDATOR_CHANGES, field="changes")
