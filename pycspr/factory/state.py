import typing

from pycspr.types import CLAccessRights
from pycspr.types import CLTypeKey
from pycspr.types import UnforgeableReference
from pycspr.types import DictionaryIdentifier_AccountNamedKey
from pycspr.types import DictionaryIdentifier_ContractNamedKey
from pycspr.types import DictionaryIdentifier_SeedURef
from pycspr.types import DictionaryIdentifier_UniqueKey
from pycspr.types import StateKey
from pycspr.types import StateKeyType
from pycspr.types import List


def create_dictionary_identifier_for_an_account_named_key(
    name: str,
    item_key: str,
    key: str
) -> DictionaryIdentifier_AccountNamedKey:
    """Returns a dictionary item identifier for querying an account's associated state.

    """
    return DictionaryIdentifier_AccountNamedKey(
        dictionary_item_key=item_key,
        dictionary_name=name,
        key=key,
        )


def create_dictionary_identifier_for_a_contract_named_key(
    key: str
) -> DictionaryIdentifier_ContractNamedKey:
    """Returns a dictionary item identifier for querying a contract's associated state.

    """
    return DictionaryIdentifier_ContractNamedKey(key=key)


def create_dictionary_identifier_for_a_seed_uref(key: str) -> DictionaryIdentifier_SeedURef:
    """Returns a dictionary item identifier for querying a uref's associated state.

    """
    return DictionaryIdentifier_SeedURef(key=key)


def create_dictionary_identifier_for_a_unique_key(key: str) -> DictionaryIdentifier_UniqueKey:
    """Returns a dictionary item identifier for querying a uref's associated state.

    """
    return DictionaryIdentifier_UniqueKey(key=key)


def create_list(items: typing.List, item_type: CLTypeKey) -> List:
    """Returns a list of items.

    """
    return List(items, item_type)


def create_state_key(identifier: bytes, typeof: StateKeyType) -> StateKey:
    """Returns a global state value key.

    """
    return StateKey(identifier, typeof)


def create_state_key_from_string(as_string: str) -> StateKey:
    """Returns a global state value key derived froma string representation.

    """
    identifier = bytes.fromhex(as_string.split("-")[-1])
    if as_string.startswith("account-hash-"):
        return create_state_key(identifier, StateKeyType.ACCOUNT)
    elif as_string.startswith("hash-"):
        return create_state_key(identifier, StateKeyType.HASH)
    elif as_string.startswith("uref-"):
        return create_state_key(identifier, StateKeyType.UREF)
    else:
        raise ValueError(f"Invalid key: {as_string}")


def create_uref_from_string(as_string: str) -> UnforgeableReference:
    """Returns an unforgeable reference from it's string representation.

    """
    _, address_hex, access_rights = as_string.split("-")

    return UnforgeableReference(
        CLAccessRights(int(access_rights)),
        bytes.fromhex(address_hex)
        )
