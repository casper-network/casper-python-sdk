import typing

from jsonrpcclient import parse, request
import requests

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

    response = requests.post(
        connection_info.address_rpc,
        json=request(constants.RPC_STATE_GET_BALANCE),
        purse_uref=purse_uref.as_string(),
        state_root_hash=state_root_hash,
        )

    return int(parse(response.json()).result["balance_value"])
