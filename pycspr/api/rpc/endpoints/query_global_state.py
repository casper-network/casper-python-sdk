import typing

from pycspr import serialisation
from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy
from pycspr.api.rpc.endpoints.chain_get_state_root_hash import exec as chain_get_state_root_hash
from pycspr.types import CL_Key
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType


_GLOBAL_STATE_ID_PARAM_NAME = {
    GlobalStateIDType.BLOCK_HASH: "BlockHash",
    GlobalStateIDType.BLOCK_HEIGHT: "BlockHeight",
    GlobalStateIDType.STATE_ROOT_HASH: "StateRootHash",
}


def exec(
    proxy: Proxy,
    key: str,
    path: typing.List[str],
    state_id: GlobalStateID = None
) -> bytes:
    """Returns results of a query to global state at a specified block or state root hash.

    :param proxy: Remote RPC server proxy.
    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :param state_id: Identifier of global state leaf.
    :returns: Results of a global state query.

    """
    if state_id is None:
        state_root: bytes = chain_get_state_root_hash()
        state_id: GlobalStateID = GlobalStateID(state_root, GlobalStateIDType.STATE_ROOT_HASH)

    return proxy.get_response(
        constants.RPC_QUERY_GLOBAL_STATE,
        get_params(key, path, state_id)
        )


def get_params(key: CL_Key, path: typing.List[str], state_id: GlobalStateID) -> dict:
    """Returns query parameters.

    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :param state_id: Identifier of global state leaf.
    :returns: RPC endpoint parameters.

    """
    try:
        state_id_type = _GLOBAL_STATE_ID_PARAM_NAME[state_id.id_type]
    except KeyError:
        raise ValueError(f"Invalid global state identifier type: {state_id.id_type}")

    if isinstance(state_id.identifier, bytes):
        state_id = state_id.identifier.hex()
    else:
        state_id = state_id.identifier

    return {
        "key": serialisation.cl_value_to_parsed(key),
        "path": path,
        "state_identifier": {
            state_id_type: state_id
        }
    }
