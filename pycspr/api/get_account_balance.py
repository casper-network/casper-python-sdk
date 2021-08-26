import typing

import jsonrpcclient as rpc_client

from pycspr import types
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    connection_info: NodeConnectionInfo,
    purse_uref: types.UnforgeableReference,
    state_root_hash: bytes = None
    ) -> typing.Union[int, dict]:
    """Returns account balance at a certain state root hash.

    :param connection_info: Information required to connect to a node.
    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Account balance if on-chain account is found.

    """
    state_root_hash = state_root_hash.hex() if state_root_hash else None

    response = rpc_client.request(
        connection_info.address_rpc,
        constants.RPC_STATE_GET_BALANCE,
        purse_uref=purse_uref.as_string(),
        state_root_hash=state_root_hash,
        )

    return int(response.data.result["balance_value"])
