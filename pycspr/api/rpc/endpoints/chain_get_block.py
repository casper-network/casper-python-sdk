from pycspr.api import constants
from pycspr.api.rpc.endpoints.utils import get_block_id
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import BlockID


def exec(proxy: Proxy, block_id: BlockID = None) -> dict:
    """Returns on-chain block information.

    :param proxy: Remote RPC server proxy.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block information.

    """
    params: dict = get_block_id(block_id, False)
    response: dict = proxy.get_response(constants.RPC_CHAIN_GET_BLOCK, params)

    return response["block"]
