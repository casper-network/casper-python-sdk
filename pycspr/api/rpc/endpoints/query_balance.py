from pycspr.api import constants
from pycspr.api.rpc.endpoints.chain_get_state_root_hash import exec as chain_get_state_root_hash
from pycspr.api.rpc.endpoints.utils import get_global_state_id
from pycspr.api.rpc.endpoints.utils import get_purse_id
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import PurseID
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType


def exec(proxy: Proxy, purse_id: PurseID, global_state_id: GlobalStateID = None) -> int:
    """Returns account balance at a certain point in global state history.

    :param proxy: Remote RPC server proxy.
    :param purse_id: Identifier of purse being queried.
    :param global_state_id: Identifier of global state root at some point in time.
    :returns: Account balance in motes (if purse exists).

    """
    if global_state_id is None:
        global_state_id = GlobalStateID(
            chain_get_state_root_hash(proxy),
            GlobalStateIDType.STATE_ROOT_HASH
        )

    params: dict = \
        get_global_state_id(global_state_id) | \
        get_purse_id(purse_id)
    response: dict = proxy.get_response(constants.RPC_QUERY_BALANCE, params)

    return int(response["balance"])
