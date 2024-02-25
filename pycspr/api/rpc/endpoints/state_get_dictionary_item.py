from pycspr.crypto import cl_checksum
from pycspr.types import DICTIONARY_ID_VARIANTS
from pycspr.types import DictionaryID
from pycspr.types import DictionaryID_AccountNamedKey
from pycspr.types import DictionaryID_ContractNamedKey
from pycspr.types import DictionaryID_SeedURef
from pycspr.types import DictionaryID_UniqueKey
from pycspr.types import StateRootID
from pycspr.api import constants
from pycspr.api.rpc.proxy import Proxy
from pycspr.api.rpc.endpoints.chain_get_state_root_hash import exec as chain_get_state_root_hash


def exec(proxy: Proxy, identifier: DictionaryID, state_root_hash: StateRootID = None) -> dict:
    """Returns on-chain data stored under a dictionary item.

    :param proxy: Remote RPC server proxy.
    :param identifier: Identifier required to query a dictionary item.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: On-chain data stored under a dictionary item.

    """
    if state_root_hash is None:
        state_root_hash = chain_get_state_root_hash(proxy)
    params: dict = get_params(identifier, state_root_hash)

    return proxy.get_response(constants.RPC_STATE_GET_DICTIONARY_ITEM, params)


def get_params(identifier: DictionaryID, state_root_hash: StateRootID) -> dict:
    """Returns JSON-RPC API request parameters.

    :param identifier: Identifier of a state dictionary.
    :param state_root_hash: A node's root state hash at some point in chain time.
    :returns: Parameters to be passed to JSON-RPC API.

    """
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
