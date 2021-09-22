from jsonrpcclient import parse, request
import requests

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
    if isinstance(identifer, type.DictionaryIdentifier_AccountNamedKey):
        response = requests.post(
            node.address_rpc,
            json=request(constants.RPC_STATE_GET_DICTIONARY_ITEM,
            {"AccountNamedKey":{
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": identifier.key
            }})
        )

    elif isinstance(identifer, type.DictionaryIdentifier_ContractNamedKey):
        response = requests.post(
            node.address_rpc,
            json=request(constants.RPC_STATE_GET_DICTIONARY_ITEM,
            {"ContractNamedKey":{
                "dictionary_item_key": identifier.dictionary_item_key,
                "dictionary_name": identifier.dictionary_name,
                "key": identifier.key
            }})
        )

    elif isinstance(identifer, type.DictionaryIdentifier_SeedURef):
        response = requests.post(
            node.address_rpc,
            json=request(constants.RPC_STATE_GET_DICTIONARY_ITEM,
            {"URef":{
                "dictionary_item_key": identifier.dictionary_item_key,
                "seed_uref": identifier.dictionary_name
            }})
        )

    elif isinstance(identifer, type.DictionaryIdentifier_UniqueKey):
        response = requests.post(
            node.address_rpc,
            json=request(constants.RPC_STATE_GET_DICTIONARY_ITEM,
            {"Dictionary":identifier.seed_uref.as_string()})
        )

    else:
        raise ValueError("Unrecognized dictionary item type.")
