import typing

from pycspr.api import constants
from pycspr.api.rpc.endpoints.chain_get_state_root_hash import exec as chain_get_state_root_hash
from pycspr.api.rpc.proxy import Proxy
from pycspr.types import StateRootID


def exec(
    proxy: Proxy,
    key: str,
    path: typing.Union[str, typing.List[str]] = [],
    state_root_hash: StateRootID = None
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

    params: dict = get_params(key, path, state_root_hash)
    response: dict = proxy.get_response(constants.RPC_STATE_GET_ITEM, params)

    return response["stored_value"]


def get_params(
    key: str,
    path: typing.Union[str, typing.List[str]],
    state_root_hash: bytes
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param key: A global state item key.
    :param path: Path(s) to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "key": key,
        "path": path,
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }
