import typing

from pycspr import types
from pycspr.serialisation.json.encoder.deploy import encode_deploy as encode_deploy_as_json


def get_account_balance_params(
    purse_uref: typing.Union[str, types.UnforgeableReference],
    state_root_hash: typing.Union[bytes, str] = None
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param purse_uref: URef of a purse associated with an on-chain account.
    :param state_root_hash: A node's root state hash at a point in chain time.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(purse_uref, types.UnforgeableReference):
        purse_uref = purse_uref.as_string()
    if isinstance(state_root_hash, bytes):
        state_root_hash = state_root_hash.hex()

    return {
        "purse_uref": purse_uref,
        "state_root_hash": state_root_hash
    }


def get_account_info_params(
    account_key: typing.Union[bytes, str],
    block_id: typing.Union[None, str, int] = None
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param account_key: Account public key prefixed with a key type identifier.
    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(account_key, bytes):
        account_key = account_key.hex()
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return {
            "public_key": account_key
        }
    elif isinstance(block_id, str):
        return {
            "public_key": account_key,
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "public_key": account_key,
            "block_identifier": {
                "Height": block_id
            }
        }


def get_auction_info_params(block_id: types.OptionalBlockIdentifer = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, str):
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }


def get_block_params(block_id: types.OptionalBlockIdentifer = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, bytes):
        return {
            "block_identifier": {
                "Hash": block_id.hex()
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }
    else:
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }


def get_block_transfers_params(block_id: typing.Union[None, str, int] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, bytes):
        return {
            "block_identifier": {
                "Hash": block_id.hex()
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }
    else:
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }


def get_deploy_params(deploy_id: typing.Union[bytes, str]) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy_id: Identifier of a deploy.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(deploy_id, bytes):
        deploy_id = deploy_id.hex()

    return {
        "deploy_hash": deploy_id
    }


def get_dictionary_item_params(identifier: types.DictionaryIdentifier) -> dict:
    """Returns JSON-RPC API request parameters.

    :param identifier: Identifier of a state dictionary.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(identifier, type.DictionaryIdentifier_AccountNamedKey):
        return {
            "AccountNamedKey": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": identifier.key
            }
        }

    elif isinstance(identifier, type.DictionaryIdentifier_ContractNamedKey):
        return {
            "ContractNamedKey": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": identifier.key
            }
        }

    elif isinstance(identifier, type.DictionaryIdentifier_SeedURef):
        return {
            "URef": {
                "dictionary_item_key": identifier.dictionary_item_key,
                "seed_uref": identifier.dictionary_name
            }
        }

    elif isinstance(identifier, type.DictionaryIdentifier_UniqueKey):
        return {
            "Dictionary": identifier.seed_uref.as_string()
        }

    else:
        raise ValueError("Unrecognized dictionary item type.")


def get_era_info_params(block_id: types.OptionalBlockIdentifer = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: JSON-RPC API parameter set.

    """
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, str):
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }


def get_state_item_params(
    item_key: str,
    item_path: typing.Union[str, typing.List[str]] = [],
    state_root_hash: bytes = None,
) -> dict:
    """Returns JSON-RPC API request parameters.

    :param item_key: A global state storage item key.
    :param item_path: Path(s) to a data held beneath the key.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "key": item_key,
        "path": item_path if isinstance(item_path, list) else [item_path],
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }


def get_state_root_hash_params(block_id: typing.Union[None, str, int] = None) -> dict:
    """Returns JSON-RPC API request parameters.

    :param block_id: Identifier of a finalised block.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    if isinstance(block_id, bytes):
        block_id = block_id.hex()

    if isinstance(block_id, type(None)):
        return None
    elif isinstance(block_id, str):
        return {
            "block_identifier": {
                "Hash": block_id
            }
        }
    elif isinstance(block_id, int):
        return {
            "block_identifier": {
                "Height": block_id
            }
        }


def put_deploy_params(deploy: types.Deploy) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy: A deploy to be dispatched to a node.
    :returns: Parameters to be passed to JSON-RPC API.

    """
    return {
        "deploy": encode_deploy_as_json(deploy)
    }
