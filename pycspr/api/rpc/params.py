import typing

from pycspr import serializer
from pycspr.crypto import checksummer
from pycspr.types.cl import CLV_Key
from pycspr.types.node.rpc import Address
from pycspr.types.node.rpc import BlockID
from pycspr.types.node.rpc import DeployHash
from pycspr.types.node.rpc import DictionaryID
from pycspr.types.node.rpc import DictionaryID_AccountNamedKey
from pycspr.types.node.rpc import DictionaryID_ContractNamedKey
from pycspr.types.node.rpc import DictionaryID_SeedURef
from pycspr.types.node.rpc import DictionaryID_UniqueKey
from pycspr.types.node.rpc import GlobalStateID
from pycspr.types.node.rpc import GlobalStateIDType
from pycspr.types.node.rpc import PurseID
from pycspr.types.node.rpc import PurseIDType
from pycspr.types.node.rpc import StateRootHash
from pycspr.utils import convertor


# Map: global state identifier type to JSON-RPC paramater name.
_GLOBAL_STATE_ID_PARAM_NAME: typing.Dict[GlobalStateIDType, str] = {
    GlobalStateIDType.BLOCK_HASH: "BlockHash",
    GlobalStateIDType.BLOCK_HEIGHT: "BlockHeight",
    GlobalStateIDType.STATE_ROOT_HASH: "StateRootHash",
}


def account_key(account_id: Address) -> dict:
    return {
        "public_key": checksummer.encode_account_key(account_id)
    }


def block_id(block_id: BlockID, allow_none=True) -> dict:
    if block_id is None:
        return dict()
    else:
        if isinstance(block_id, (bytes, str)):
            return {
                "block_identifier": {
                    "Hash": checksummer.encode_block_id(block_id)
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


def deploy_hash(deploy_hash: DeployHash) -> dict:
    return {
        "deploy_hash": checksummer.encode_deploy_hash(deploy_hash)
    }


def global_state_id(global_state_id: GlobalStateID) -> dict:
    id = \
        global_state_id.identifier.hex() if isinstance(global_state_id.identifier, bytes) else \
        global_state_id.identifier

    return {
        global_state_id.id_type.value: id
    }


def for_query_global_state(
    key: CLV_Key,
    path: typing.List[str],
    state_id: GlobalStateID
) -> dict:
    if isinstance(state_id.identifier, bytes):
        state_id = state_id.identifier.hex()
    else:
        state_id = state_id.identifier

    return {
        "key": serializer.cl_value_to_parsed(key),
        "path": path,
        "state_identifier": {
            state_id.id_type.value: state_id
        }
    }


def for_state_get_dictionary_item(
    identifier: DictionaryID,
    state_root_hash: StateRootHash
) -> dict:
    def get_dictionary_param():
        if isinstance(identifier, DictionaryID_AccountNamedKey):
            return {
                "AccountNamedKey": {
                    "dictionary_item_key": identifier.dictionary_item_key,
                    "dictionary_name": identifier.dictionary_name,
                    "key": f"hash-{checksummer.encode_account_id(identifier.account_key)}"
                }
            }
        elif isinstance(identifier, DictionaryID_ContractNamedKey):
            return {
                "ContractNamedKey": {
                    "dictionary_item_key": identifier.dictionary_item_key,
                    "dictionary_name": identifier.dictionary_name,
                    "key": f"hash-{checksummer.encode_contract_id(identifier.contract_key)}"
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
        else:
            raise ValueError("Unrecognized dictionary item type.")

    return {
        "dictionary_identifier": get_dictionary_param(),
        "state_root_hash": state_root_hash.hex(),
    }


def for_state_get_item(
    key: str,
    path: typing.Union[str, typing.List[str]],
    state_root_hash: bytes
) -> dict:
    return {
        "key": key,
        "path": path,
        "state_root_hash": state_root_hash.hex() if state_root_hash else None
    }


def purse_id(purse_id: PurseID) -> dict:
    id = \
        purse_id.identifier.hex() if isinstance(purse_id.identifier, bytes) else \
        purse_id.identifier
    

    if purse_id.id_type == PurseIDType.ACCOUNT_HASH:
        return {
            "purse_identifier": {
                "main_purse_under_account_hash": f"{convertor.str_from_account_key(id)}"
            }
        }
    elif purse_id.id_type == PurseIDType.PUBLIC_KEY:
        return {
            "purse_identifier": {
                "main_purse_under_public_key": id
            }
        }
    elif purse_id.id_type == PurseIDType.UREF:
        return {
            "purse_identifier": {
                "purse_uref": convertor.str_from_uref(purse_id.identifier)
            }
        }
    else:
        raise ValueError(f"Invalid purse identifier type: {purse_id.id_type}")
