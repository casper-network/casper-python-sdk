import typing

import jsonrpcclient as rpc_client

from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    item_key: str,
    item_path: typing.Union[str, typing.List[str]] = [],
    state_root_hash: bytes = None,
    ) -> dict:
    """Returns result of a chain query a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param item_key: A global state storage item key.
    :param item_path: Path(s) to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Query result in JSON format.

    """
    item_path = item_path if isinstance(item_path, list) else [item_path]
    state_root_hash = state_root_hash.hex() if state_root_hash else None
    response = rpc_client.request(
        connection_info.address_rpc,
        constants.RPC_STATE_GET_ITEM,
        key=item_key,
        path=item_path,
        state_root_hash=state_root_hash,
        )

    return response.data.result["stored_value"]
