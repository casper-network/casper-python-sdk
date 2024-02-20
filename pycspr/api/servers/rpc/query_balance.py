from pycspr import types
from pycspr.api import constants
from pycspr.api.servers.rpc import utils
from pycspr.api.servers.rpc.chain_get_state_root_hash import exec as chain_get_state_root_hash


def exec(
    proxy: utils.Proxy,
    purse_id: types.PurseID,
    global_state_id: types.GlobalStateID = None
) -> int:
    """Returns account balance at a certain point in global state history.

    :param proxy: Remote RPC server proxy. 
    :param purse_id: Identifier of purse being queried.
    :param global_state_id: Identifier of global state root at some point in time.
    :returns: Account balance in motes (if purse exists).

    """
    params: dict = get_params(proxy, purse_id, global_state_id)
    response: dict = proxy.get_response(constants.RPC_QUERY_BALANCE, params)

    return int(response["balance"])


def get_params(
    proxy: utils.Proxy,
    purse_id: types.PurseID,
    global_state_id: types.GlobalStateID=None
) -> dict:
    if global_state_id is None:
        global_state_id = types.GlobalStateID(
            chain_get_state_root_hash(proxy),
            types.GlobalStateIDType.STATE_ROOT_HASH
        )

    return utils.get_global_state_id(global_state_id) | \
           utils.get_purse_id(purse_id)
