import typing

from pycspr import serialisation
from pycspr import types
from pycspr.api import constants
from pycspr.api.servers.rpc import utils
from pycspr.api.servers.rpc.chain_get_state_root_hash import exec as chain_get_state_root_hash


def exec(
    proxy: utils.Proxy,
    key: str,
    path: typing.Union[str, typing.List[str]] = [],
    state_root_hash: types.StateRootHash = None
) -> bytes:
    """Returns results of a query to global state at a specified block or state root hash.

    :param proxy: Remote RPC server proxy. 
    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Results of a global state query.

    """
    path = path if isinstance(path, list) else [path]
    state_root_hash = state_root_hash or chain_get_state_root_hash(proxy)

    params = get_params(key, path, state_root_hash)
    response = proxy.get_response(constants.RPC_STATE_GET_ITEM, params)

    return response["stored_value"]


def get_params(
    state_id: types.GlobalStateID,
    key: types.CL_Key,
    path: typing.List[str]
) -> dict:
    """Returns results of a query to global state at a specified block or state root hash.

    :param state_id: Identifier of global state leaf.
    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :returns: Parameters to be passed to endpoint.

    """
    if state_id.id_type == types.GlobalStateIDType.BLOCK_HASH:
        state_id_type = "BlockHash"
    elif state_id.id_type == types.GlobalStateIDType.BLOCK_HEIGHT:
        state_id_type = "BlockHash"
    elif state_id.id_type == types.GlobalStateIDType.STATE_ROOT_HASH:
        state_id_type = "StateRootHash"
    else:
        raise ValueError(f"Invalid global state identifier type: {state_id.id_type}")

    state_id = \
        state_id.identifier.hex() if isinstance(state_id.identifier, bytes) else \
        state_id.identifier

    return {
        "state_identifier": {
            state_id_type: state_id
        },
        "key": serialisation.cl_value_to_parsed(key),
        "path": path
    }


def get_state_item_params(
    item_key: str,
    item_path: typing.Union[str, typing.List[str]] = [],
    state_root_hash: bytes = None,
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param item_key: A global state item key.
    :param item_path: Path(s) to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    item_path = item_path if isinstance(item_path, list) else [item_path]

    return {
        "key": item_key,
        "path": item_path,
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }
