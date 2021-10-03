from typing import Union

from pycspr.types import UnforgeableReference
from pycspr.api.constants import RPC_STATE_GET_BALANCE

"""
Returns account balance at a certain state root hash.

:param node: Encapsulates interaction with a remote node.
:param purse_uref: URef of a purse associated with an on-chain account.
:param state_root_hash: A node's root state hash at some point in
                        chain time.
:returns: Account balance if on-chain account is found.
"""


def get_rpc_name():
    return RPC_STATE_GET_BALANCE


def extract_result(response):
    return int(response["balance_value"])


def get_params(purse_uref: Union[str, UnforgeableReference],
               state_root_hash: Union[bytes, str] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in
                            chain time.
    :returns: Parameters to be passed to JSON-RPC API.
    """
    if isinstance(purse_uref, UnforgeableReference):
        purse_uref = purse_uref.as_string()
    if isinstance(state_root_hash, bytes):
        state_root_hash = state_root_hash.hex()
    return {
        "purse_uref": purse_uref,
        "state_root_hash": state_root_hash
    }
