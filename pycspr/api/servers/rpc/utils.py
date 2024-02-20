import dataclasses

import jsonrpcclient
import requests

from pycspr import serialisation
from pycspr import types
from pycspr.api import constants
from pycspr.crypto import cl_checksum


@dataclasses.dataclass
class Proxy:
    """Node JSON-RPC server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed REST port.
    port: int = constants.DEFAULT_PORT_RPC

    @property
    def address(self) -> str:
        """A node's RPC server base address."""
        return f"http://{self.host}:{self.port}/rpc"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def get_response(self, endpoint: str, params: dict = None) -> dict:
        """Invokes remote speculative JSON-RPC API and returns parsed response.

        :endpoint: Target endpoint to invoke.
        :params: Endpoint parameters.
        :returns: Parsed JSON-RPC response.

        """
        request = jsonrpcclient.request(endpoint, params)
        response = requests.post(self.address, json=request)
        response_parsed = jsonrpcclient.parse(response.json())
        if isinstance(response_parsed, jsonrpcclient.responses.Error):
            raise ProxyError(response_parsed)

        return response_parsed.result


class ProxyError(Exception):
    """Node API error wrapper.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(ProxyError, self).__init__(msg)


def get_block_id(block_id: types.BlockID, allow_none=True) -> dict:
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


def get_account_key(account_id: types.AccountID) -> dict:
    return {
        "public_key": cl_checksum.encode_account_key(account_id)
    }


def get_deploy_id(deploy_id: types.DeployID) -> dict:
    return {
        "deploy_hash": cl_checksum.encode_deploy_id(deploy_id)
    }


def get_purse_id(purse_id: types.PurseID) -> dict:
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


def get_global_state_id(global_state_id: types.GlobalStateID) -> dict:
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
