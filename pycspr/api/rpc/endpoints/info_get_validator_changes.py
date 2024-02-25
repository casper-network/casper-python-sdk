from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import StateRootID


def exec(proxy: Proxy) -> StateRootID:
    """Returns validator change set.

    :param proxy: Remote RPC server proxy.
    :returns: Validator change set.

    """
    response: dict = proxy.get_response(constants.RPC_INFO_GET_VALIDATOR_CHANGES)

    return response["changes"]
