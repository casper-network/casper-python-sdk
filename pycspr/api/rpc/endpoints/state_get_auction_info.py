from pycspr.api import constants
from pycspr.api.rpc.endpoints import utils
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import BlockID


def exec(proxy: Proxy, block_id: BlockID = None) -> dict:
    """Returns current auction system contract information.

    :param proxy: Remote RPC server proxy.
    :param block_id: Identifier of a finalised block.
    :returns: Current auction system contract information.

    """
    params: dict = utils.get_block_id(block_id, False)

    return proxy.get_response(constants.RPC_STATE_GET_AUCTION_INFO, params, "auction_state")
