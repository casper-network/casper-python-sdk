import typing

from pycspr import serialisation
from pycspr.crypto import cl_checksum
from pycspr.types import AccountID
from pycspr.types import BlockID
from pycspr.types import CL_Key
from pycspr.types import DeployID
from pycspr.types import DICTIONARY_ID_VARIANTS
from pycspr.types import DictionaryID
from pycspr.types import DictionaryID_AccountNamedKey
from pycspr.types import DictionaryID_ContractNamedKey
from pycspr.types import DictionaryID_SeedURef
from pycspr.types import DictionaryID_UniqueKey
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType
from pycspr.types import PurseID
from pycspr.types import PurseIDType
from pycspr.types import StateRootID


# Map: global state identifier type to JSON-RPC paramater name.
_GLOBAL_STATE_ID_PARAM_NAME: typing.Dict[GlobalStateIDType, str] = {
    GlobalStateIDType.BLOCK_HASH: "BlockHash",
    GlobalStateIDType.BLOCK_HEIGHT: "BlockHeight",
    GlobalStateIDType.STATE_ROOT_HASH: "StateRootHash",
}


def get_block_id(block_id: BlockID, allow_none=True) -> dict:
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


def get_account_key(account_id: AccountID) -> dict:
    return {
        "public_key": cl_checksum.encode_account_key(account_id)
    }


def get_deploy_id(deploy_id: DeployID) -> dict:
    return {
        "deploy_hash": cl_checksum.encode_deploy_id(deploy_id)
    }


def get_purse_id(purse_id: PurseID) -> dict:
    id = \
        purse_id.identifier.hex() if isinstance(purse_id.identifier, bytes) else \
        purse_id.identifier

    if purse_id.id_type == PurseIDType.ACCOUNT_HASH:
        id = f"account-hash-{id}"
        id_type = "main_purse_under_account_hash"
    elif purse_id.id_type == PurseIDType.PUBLIC_KEY:
        id_type = "main_purse_under_public_key"
    elif purse_id.id_type == PurseIDType.UREF:
        id = serialisation.cl_value_to_parsed(purse_id.identifier)
        id_type = "purse_uref"
    else:
        raise ValueError(f"Invalid purse identifier type: {purse_id.id_type}")

    return {
        "purse_identifier": {
            id_type: id
        }
    }


def get_global_state_id(global_state_id: GlobalStateID) -> dict:
    id = \
        global_state_id.identifier.hex() if isinstance(global_state_id.identifier, bytes) else \
        global_state_id.identifier

    if global_state_id.id_type == GlobalStateIDType.BLOCK_HASH:
        id_type = "BlockHash"
    elif global_state_id.id_type == GlobalStateIDType.BLOCK_HEIGHT:
        id_type = "BlockHash"
    elif global_state_id.id_type == GlobalStateIDType.STATE_ROOT_HASH:
        id_type = "StateRootHash"
    else:
        raise ValueError(f"Invalid global state identifier type: {global_state_id.id_type}")

    return {
        id_type: id
    }


def get_params_for_query_global_state(
    key: CL_Key,
    path: typing.List[str],
    state_id: GlobalStateID
) -> dict:
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


def get_params_for_state_get_dictionary_item(
    identifier: DictionaryID,
    state_root_hash: StateRootID
) -> dict:
    def get_dictionary_param():
        if not isinstance(identifier, DICTIONARY_ID_VARIANTS):
            raise ValueError("Unrecognized dictionary item type.")
        elif isinstance(identifier, DictionaryID_AccountNamedKey):
            return {
                "AccountNamedKey": {
                    "dictionary_item_key": identifier.dictionary_item_key,
                    "dictionary_name": identifier.dictionary_name,
                    "key": f"hash-{cl_checksum.encode_account_id(identifier.account_key)}"
                }
            }
        elif isinstance(identifier, DictionaryID_ContractNamedKey):
            return {
                "ContractNamedKey": {
                    "dictionary_item_key": identifier.dictionary_item_key,
                    "dictionary_name": identifier.dictionary_name,
                    "key": f"hash-{cl_checksum.encode_contract_id(identifier.contract_key)}"
                }
            }
        elif isinstance(identifier, DictionaryID_SeedURef):
            return {
                "URef": {
                    "dictionary_item_key": identifier.dictionary_item_key,
                    "seed_uref": identifier.dictionary_name
                }
            }
        elif isinstance(identifier, DictionaryID_UniqueKey):
            return {
                "Dictionary": identifier.seed_uref.as_string()
            }

    return {
        "dictionary_identifier": get_dictionary_param(),
        "state_root_hash": state_root_hash.hex(),
    }


def get_params_for_state_get_item(
    key: str,
    path: typing.Union[str, typing.List[str]],
    state_root_hash: bytes
) -> dict:
    return {
        "key": key,
        "path": path,
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }
