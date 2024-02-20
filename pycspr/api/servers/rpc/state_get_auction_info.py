from pycspr import types
from pycspr.api import constants
from pycspr.api.servers.rpc import utils


def exec(proxy: utils.Proxy, block_id: types.BlockID = None) -> dict:
    """Returns current auction system contract information.

    :returns: Current auction system contract information.

    """
    params: dict = utils.get_block_id(block_id, False)

    return proxy.get_response(constants.RPC_STATE_GET_AUCTION_INFO, params)
