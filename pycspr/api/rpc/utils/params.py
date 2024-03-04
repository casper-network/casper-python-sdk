from pycspr import serialisation
from pycspr.crypto import cl_checksum
from pycspr.types import AccountID
from pycspr.types import BlockID
from pycspr.types import DeployID
from pycspr.types import GlobalStateID
from pycspr.types import GlobalStateIDType
from pycspr.types import PurseID
from pycspr.types import PurseIDType


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
