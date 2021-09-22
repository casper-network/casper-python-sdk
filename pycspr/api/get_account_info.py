import typing

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    account_key: bytes,
    block_id: typing.Union[None, bytes, str, int] = None
    ) -> dict:
    """Returns on-chain account information at a certain state root hash.

    :param node: Information required to connect to a node.
    :param account_key: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Account information in JSON format.

    """    
    params = get_params(account_key, block_id)
    response = node.get_response(constants.RPC_STATE_GET_ACCOUNT_INFO, params)

    return response["account"]


def get_params(
    account_key: bytes,
    block_id: typing.Union[None, str, int] = None
    ) -> dict:
    """Returns JSON-RPC API request parameters.

    :param account_key: An account holder's public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, type(None)):
        return {
            "public_key":account_key.hex()
        }

    elif isinstance(block_id, (bytes, str)):
        return {
            "public_key":account_key.hex(),
            "block_identifier":{
                "Hash": block_id.hex() if isinstance(block_id, bytes) else block_id
            }            
        }

    elif isinstance(block_id, int):
        return {
            "public_key":account_key.hex(),
            "block_identifier":{
                "Height": block_id
            }            
        }
