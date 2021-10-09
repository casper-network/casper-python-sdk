import typing

from pycspr.api import constants
from pycspr.api.utils import get_block_id_param
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain block information.

    :param node: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: On-chain block information.

    """
    params = get_params(block_id)
    response = node.get_response(constants.RPC_CHAIN_GET_BLOCK, params)

    return response["block"]


def get_params(block_id: typing.Union[None, str, int] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    param = get_block_id_param(block_id)
    return param
