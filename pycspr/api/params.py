import typing

from pycspr import serialisation
from pycspr import types
from pycspr.crypto import cl_checksum
from pycspr.types import DICTIONARY_ID_VARIANTS
from pycspr.types.cl_values import CL_Key


def get_account_info_params(account_id: types.AccountID, block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param account_key: Account public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    return _get_params_of_block_id(block_id) | _get_params_of_account_key(account_id)


def get_auction_info_params(block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    return _get_params_of_block_id(block_id, False)


def get_block_params(block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    return _get_params_of_block_id(block_id, False)


def get_block_transfers_params(block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return _get_params_of_block_id(block_id, False)


def get_deploy_params(deploy_id: types.DeployID) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy_id: Identifier of a deploy.
    :returns: JSON-RPC API parameter set.

    """
    return _get_params_of_deploy_id(deploy_id)


def get_dictionary_item_params(identifier: types.DictionaryID, state_root_hash: bytes) -> dict:
    """Returns JSON-RPC API request parameters.

    :param identifier: Identifier of a state dictionary.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if not isinstance(identifier, DICTIONARY_ID_VARIANTS):
        raise ValueError("Unrecognized dictionary item type.")

    result: dict = {
        "state_root_hash": state_root_hash.hex(),
    }

    if isinstance(identifier, types.DictionaryID_AccountNamedKey):
        result["dictionary_identifier"] = {
            "AccountNamedKey": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": f"hash-{cl_checksum.encode_account_id(identifier.account_key)}"
            }
        }

    elif isinstance(identifier, types.DictionaryID_ContractNamedKey):
        result["dictionary_identifier"] = {
            "ContractNamedKey": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": f"hash-{cl_checksum.encode_contract_id(identifier.contract_key)}"
            }
        }

    elif isinstance(identifier, types.DictionaryID_SeedURef):
        result["dictionary_identifier"] = {
            "URef": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "seed_uref": identifier.dictionary_name
            }
        }

    elif isinstance(identifier, types.DictionaryID_UniqueKey):
        result["dictionary_identifier"] = {
            "Dictionary": identifier.seed_uref.as_string()
        }

    return result


def get_era_info_params(block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    return _get_params_of_block_id(block_id)


def get_era_summary_params(block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    return _get_params_of_block_id(block_id)


def get_query_balance_params(
    global_state_id: types.GlobalStateID,
    purse_id: types.PurseID
) -> dict:
    """Returns results of a query to global state at a specified block or state root hash.

    :param state_id: Identifier of global state leaf.
    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :returns: Results of a global state query.

    """
    return _get_params_of_global_state_id(global_state_id) | \
           _get_params_of_purse_id(purse_id)


def get_query_global_state_params(
    state_id: types.GlobalStateID,
    key: CL_Key,
    path: typing.List[str]
) -> dict:
    """Returns results of a query to global state at a specified block or state root hash.

    :param state_id: Identifier of global state leaf.
    :param key: Key of an item stored within global state.
    :param path: Identifier of a path within item.
    :returns: Results of a global state query.

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


def get_state_root_hash_params(block_id: types.BlockID = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return _get_params_of_block_id(block_id)


def put_deploy_params(deploy: types.Deploy) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy: A deploy to be dispatched to a node.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "deploy": serialisation.to_json(deploy)
    }


def speculative_exec_params(
    deploy: types.Deploy,
    block_id: types.BlockID = None
    ) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy: A deploy to be dispatched to a node.
    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, (bytes, str)):
        return {
            "block_identifier": {
                "Hash": cl_checksum.encode_block_id(block_id)
            },
            "deploy": serialisation.to_json(deploy)
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            },
            "deploy": serialisation.to_json(deploy)
        }
    else:
        return {
            "block_identifier": None,
            "deploy": serialisation.to_json(deploy)
        }


def _get_params_of_block_id(block_id: types.BlockID, allow_none=True) -> dict:
    if block_id is not None:
        if isinstance(block_id, (bytes, str)):
            return {
                "block_identifier": {
                    "Hash": cl_checksum.encode_block_id(block_id)
                }
            }
        elif isinstance(block_id, int):
            return {
                "block_identifier": {
                    "Height": block_id
                }
            }
        elif allow_none is True:
            return {
                "block_identifier": None
            }
    else:
        return dict()


def _get_params_of_account_key(account_id: types.AccountID) -> dict:
    return {
        "public_key": cl_checksum.encode_account_key(account_id)
    }


def _get_params_of_deploy_id(deploy_id: types.DeployID) -> dict:
    return {
        "deploy_hash": cl_checksum.encode_deploy_id(deploy_id)
    }


def _get_params_of_purse_id(purse_id: types.PurseID) -> dict:
    id = \
        purse_id.identifier.hex() if isinstance(purse_id.identifier, bytes) else \
        purse_id.identifier

    if purse_id.id_type == types.PurseIDType.ACCOUNT_HASH:
        id = f"account-hash-{id}"
        id_type = "main_purse_under_account_hash"
    elif purse_id.id_type == types.PurseIDType.PUBLIC_KEY:
        id_type = "main_purse_under_public_key"
    elif purse_id.id_type == types.PurseIDType.UREF:
        id = serialisation.cl_value_to_parsed(purse_id.identifier)
        id_type = "purse_uref"
    else:
        raise ValueError(f"Invalid purse identifier type: {purse_id.id_type}")

    return {
        "purse_identifier": {
            id_type: id
        }
    }


def _get_params_of_global_state_id(global_state_id: types.GlobalStateID) -> dict:
    id = \
        global_state_id.identifier.hex() if isinstance(global_state_id.identifier, bytes) else \
        global_state_id.identifier

    if global_state_id.id_type == types.GlobalStateIDType.BLOCK_HASH:
        id_type = "BlockHash"
    elif global_state_id.id_type == types.GlobalStateIDType.BLOCK_HEIGHT:
        id_type = "BlockHash"
    elif global_state_id.id_type == types.GlobalStateIDType.STATE_ROOT_HASH:
        id_type = "StateRootHash"
    else:
        raise ValueError(f"Invalid global state identifier type: {global_state_id.id_type}")

    return {
        id_type: id
    }
