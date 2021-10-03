from typing import Union, List

from pycspr.api.constants import RPC_STATE_GET_ITEM
from pycspr.client import NodeConnectionInfo

"""
Returns result of a chain query a certain state root hash.

:param node: Information required to connect to a node.
:param item_key: A global state storage item key.
:param item_path: Path(s) to a data held beneath the key.
:param state_root_hash: A node's root state hash at some point in
                        chain time.
:returns: Query result in JSON format.
"""


def get_rpc_name():
    return RPC_STATE_GET_ITEM


def extract_result(response):
    return response["stored_value"]


def get_params(item_key: str,
               item_path: Union[str, List[str]] = [],
               state_root_hash: bytes = None) -> dict:
    """
    Returns JSON-RPC API request parameters.

    :param item_key: A global state storage item key.
    :param item_path: Path(s) to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in
                            chain time.
    :returns: Parameters to be passed to JSON-RPC API.
    """
    return {
        "key": item_key,
        "path": item_path if isinstance(item_path, list) else [item_path],
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }
