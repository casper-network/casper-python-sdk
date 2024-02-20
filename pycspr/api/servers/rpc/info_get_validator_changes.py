from pycspr import types
from pycspr.api import constants
from pycspr.api.servers.rpc.utils import Proxy


def exec(proxy: Proxy) -> types.StateRootHash:
    """Returns root hash of global state at a finalised block.

    :returns: State root hash at finalised block.

    """
    response = proxy.get_response(constants.RPC_INFO_GET_VALIDATOR_CHANGES)

    return response["changes"]
