import dataclasses
import enum
from pycspr.types.cl import CLAccessRights


@dataclasses.dataclass
class UnforgeableReference():
    """An unforgeable reference storage key.

    """
    # Uref on-chain identifier.
    address: bytes

    # Access rights granted by issuer.
    access_rights: CLAccessRights

    def as_string(self):
        """Returns a string representation for over the wire dispatch.

        """
        return f"uref-{self.address.hex()}-{self.access_rights.value:03}"


@dataclasses.dataclass
class DictionaryIdentifier():
    """A set of variants for performation dictionary item state queries.

    """
    pass


@dataclasses.dataclass
class DictionaryIdentifier_AccountNamedKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via an Account's named keys.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    # The account key as a formatted string whose named keys contains dictionary_name.
    key: str


@dataclasses.dataclass
class DictionaryIdentifier_ContractNamedKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via a Contract's named keys.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    # The contract key as a formatted string whose named keys contains dictionary_name.
    key: str


@dataclasses.dataclass
class DictionaryIdentifier_SeedURef(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item
       via it's seed unforgeable reference.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The dictionary's seed URef.
    seed_uref: UnforgeableReference


@dataclasses.dataclass
class DictionaryIdentifier_UniqueKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via it's unique key.

    """
    # The globally unique dictionary key.
    key: str


class StorageKeyType(enum.Enum):
    """Enumeration over set of CL storage key.

    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2


@dataclasses.dataclass
class StorageKey():
    """A pointer to data within global state.

    """
    # 32 byte key identifier.
    identifier: bytes

    # Key type identifier.
    typeof: StorageKeyType

    def as_string(self):
        """Returns a string representation for over the wire dispatch.

        """
        _PREFIXES = {
            StorageKeyType.ACCOUNT: "account-hash",
            StorageKeyType.HASH: "hash",
            StorageKeyType.UREF: "uref"
        }

        return f"{_PREFIXES[self.typeof]}-{self.identifier.hex()}"
