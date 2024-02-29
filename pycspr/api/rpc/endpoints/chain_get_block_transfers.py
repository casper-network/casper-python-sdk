from pycspr.api import constants
from pycspr.api.rpc.endpoints import utils
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import BlockID


def exec(proxy: Proxy, block_id: BlockID = None) -> dict:
    """Returns identifiers of set of transfers contained within a block.

    :param proxy: Remote RPC server proxy.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block transfers information.

    """
    params: dict = utils.get_block_id(block_id, False)

    return proxy.get_response(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS, params)
