import typing

import jsonrpcclient as rpc_client

from pycspr.client import NodeConnectionInfo



# RPC method to be invoked.
# TODO: use new endpoint -> state_get_account_info
_API_ENDPOINT = "state_get_item"



def execute(
    connection_info: NodeConnectionInfo,
    account_hash: bytes,
    state_root_hash: typing.Union[bytes, None] = None
    ) -> dict:
    """Returns on-chain account information at a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param account_hash: An on-chain account identifier derived from it's associated public key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Account information in JSON format.

    """    
    key=f"account-hash-{account_hash.hex()}"
    path = []
    state_root_hash = state_root_hash.hex() if state_root_hash else None

    response = rpc_client.request(
        connection_info.address_rpc,
        _API_ENDPOINT,
        key=key,
        path=path,
        state_root_hash=state_root_hash
        )

    return response.data.result["stored_value"]["Account"]
