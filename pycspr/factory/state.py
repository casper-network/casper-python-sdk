from pycspr.types import CLAccessRights
from pycspr.types import UnforgeableReference
from pycspr.types import DictionaryIdentifier_AccountNamedKey
from pycspr.types import DictionaryIdentifier_ContractNamedKey
from pycspr.types import DictionaryIdentifier_SeedURef
from pycspr.types import DictionaryIdentifier_UniqueKey
from pycspr.types import StorageKey
from pycspr.types import StorageKeyType


def create_uref_from_string(as_string: str):
    """Returns an unforgeable reference from it's string representation.

    """
    _, address_hex, access_rights = as_string.split("-")

    return UnforgeableReference(
        bytes.fromhex(address_hex),
        CLAccessRights(int(access_rights))
        )


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


def create_storage_key(identifier: bytes, typeof: StorageKeyType) -> StorageKey:
    return StorageKey(identifier, typeof)
