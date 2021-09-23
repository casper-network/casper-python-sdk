from pycspr import types
from pycspr.api import constants
from pycspr.client import NodeConnectionInfo



def execute(
    node: NodeConnectionInfo,
    identifier: types.DictionaryIdentifier
    ) -> dict:
    """Returns on-chain data stored under a dictionary item.

    :param node: Information required to connect to a node.
    :param identifier: Identifier required to query a dictionary item.
    :returns: On-chain data stored under a dictionary item.

    """
    params = get_parms(identifier)

    return node.get_response(constants.RPC_STATE_GET_DICTIONARY_ITEM, params)


def get_params(identifier: types.DictionaryIdentifier) -> dict:
    """Returns JSON-RPC API request parameters.

    :param deploy_id: Identifier of a queued/processed deploy.
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

