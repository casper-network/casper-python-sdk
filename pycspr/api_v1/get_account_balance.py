import typing

import jsonrpcclient as rpc_client

from pycspr.types import NodeConnectionInfo



# RPC method to be invoked.
_API_ENDPOINT = "state_get_balance"


def execute(
    connection_info: NodeConnectionInfo,
    purse_uref: str,
    state_root_hash: bytes = None,
    parse_response: bool = True,
    ) -> typing.Union[int, dict]:
    """api account balance at a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Account balance if on-chain account is found.

    """
    state_root_hash = state_root_hash.hex() if state_root_hash else None

    response = rpc_client.request(
        connection_info.address_rpc,
        _API_ENDPOINT,
        purse_uref=purse_uref,
        state_root_hash=state_root_hash,
        )

    if parse_response:
        response = int(response.data.result["balance_value"])
    
    return response
