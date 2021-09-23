import typing

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> str:
    """Returns an on-chain state root hash at specified block.

    :param node: Information required to connect to a node.
    :param block_id: Identifier of a finalised block.
    :returns: State root hash at specified block.

    """
    params = get_params(block_id)
    response = node.get_response(constants.RPC_CHAIN_GET_STATE_ROOT_HASH, params)

    return response["state_root_hash"]


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
