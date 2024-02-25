from pycspr.api import constants
from pycspr.api.rpc.endpoints.utils import get_block_id
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import BlockID


def exec(proxy: Proxy, block_id: BlockID = None) -> dict:
    """Returns current auction system contract information.

    :returns: Current auction system contract information.

    """
    params: dict = get_block_id(block_id, False)

    return proxy.get_response(constants.RPC_STATE_GET_AUCTION_INFO, params)
