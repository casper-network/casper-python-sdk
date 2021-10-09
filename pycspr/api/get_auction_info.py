import typing

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo
from pycspr.api.utils import get_block_id_param



def execute(
    node: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns current auction system contract information.

    :param node: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: Current auction system contract information.

    """
    params = get_params(block_id)

    return node.get_response(constants.RPC_STATE_GET_AUCTION_INFO, params)


def get_params(block_id: typing.Union[None, str, int] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    param = get_block_id_param(block_id)
    return param
