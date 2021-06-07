import typing

import jsonrpcclient as rpc_client

import pycspr
from pycspr.crypto import get_account_hash



# RPC method to be invoked.
_API_ENDPOINT = "state_get_balance"


def execute(
    purse_uref: str,
    state_root_hash: str = None,
    parse_response: bool = True,
    ) -> typing.Union[int, dict]:
    """api account balance at a certain state root hash.

    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :param parse_response: Flag indicating whether to parse web-service response.

    :returns: Account balance if on-chain account is found.

    """
    response = rpc_client.request(pycspr.CONNECTION.address_rpc, _API_ENDPOINT,
        purse_uref=purse_uref,
        state_root_hash=state_root_hash,
        )
    
    return int(response.data.result["balance_value"]) if parse_response else response.data.result
