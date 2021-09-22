import typing

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



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
    if isinstance(block_id, type(None)):
        return None

    elif isinstance(block_id, (bytes, str)):
        return {
            "block_identifier":{
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }            
        }

    elif isinstance(block_id, int):
        return {
            "block_identifier":{
                "Height": block_id
            }            
        }
