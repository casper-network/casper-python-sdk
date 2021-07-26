import typing

import jsonrpcclient as rpc_client

from pycspr.client import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "state_get_item"


def execute(
    connection_info: NodeConnectionInfo,
    key: str,
    path: typing.List[str] = [],
    state_root_hash: bytes = None,
    ) -> dict:
    """Returns reault of a chain query a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param key: A global state storage item key.
    :param path: Path to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Query result in JSON format.

    """ 
    state_root_hash = state_root_hash.hex() if state_root_hash else None
    response = rpc_client.request(connection_info.address_rpc, _API_ENDPOINT,
        key=key,
        path=[],
        state_root_hash=state_root_hash,
        )

    return response.data.result
