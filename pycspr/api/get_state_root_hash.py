import typing

from pycspr.api.utils import get_block_id_param
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    block_id: typing.Union[bytes, str, int] = None
    ) -> str:
    """Returns an on-chain state root hash at specified block.

    :param node: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: State root hash at specified block.

    """
    params = get_params(block_id)
    response = node.get_response(constants.RPC_CHAIN_GET_STATE_ROOT_HASH, params)

    return response["state_root_hash"]


def get_params(block_id: typing.Union[str, int] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    param = get_block_id_param(block_id)
    return param
