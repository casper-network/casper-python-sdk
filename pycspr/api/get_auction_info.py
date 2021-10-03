from typing import Union
from pycspr.api.constants import RPC_STATE_GET_AUCTION_INFO

"""
Returns current auction system contract information.

:param node: Information required to connect to a node.
:param block_id: Identifier of a finalised block.
:returns: Current auction system contract information.
"""


def get_rpc_name():
    return RPC_STATE_GET_AUCTION_INFO


def extrac_result(response):
    return response


def get_params(block_id: Union[None, str, int] = None) -> dict:
    """
    Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.
    """
    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, (bytes, str)):
        return {
            "block_identifier": {
                "Hash": block_id.hex()
                if isinstance(block_id, bytes) else block_id
                }
            }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
                }
            }
