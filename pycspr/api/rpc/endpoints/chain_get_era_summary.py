from pycspr.api import constants
from pycspr.api.rpc.endpoints import utils
from pycspr.api.rpc.proxy import Proxy
from pycspr.api.rpc.types import EraSummary
from pycspr.types import BlockID


def exec(proxy: Proxy, block_id: BlockID = None) -> EraSummary:
    """Returns consensus era summary information.

    :param proxy: Remote RPC server proxy.
    :param block_id: Identifier of a block.
    :returns: Era summary information.

    """
    params: dict = utils.get_block_id(block_id, False)

    return proxy.get_response(constants.RPC_CHAIN_GET_ERA_SUMMARY, params, "era_summary")
