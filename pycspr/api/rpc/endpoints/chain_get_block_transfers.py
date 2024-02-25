import typing

from pycspr.api import constants
from pycspr.api.rpc.endpoints.utils import get_block_id
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import BlockID
from pycspr.types import DeployID


def exec(proxy: Proxy, block_id: BlockID = None) -> typing.Tuple[BlockID, typing.List[DeployID]]:
    """Returns identifiers of set of transfers contained within a block.

    :param proxy: Remote RPC server proxy.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block transfers information.

    """
    params: dict = get_block_id(block_id, False)
    response: dict = proxy.get_response(constants.RPC_CHAIN_GET_BLOCK_TRANSFERS, params)

    return (response["block_hash"], response["transfers"])
