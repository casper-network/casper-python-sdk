from pycspr.api import constants
from pycspr.api.servers.rpc.utils.proxy import Proxy
from pycspr.types import StateRootHash


def exec(proxy: Proxy) -> StateRootHash:
    """Returns root hash of global state at a finalised block.

    :param proxy: Remote RPC server proxy.
    :returns: State root hash at finalised block.

    """
    response: dict = proxy.get_response(constants.RPC_INFO_GET_VALIDATOR_CHANGES)

    return response["changes"]
