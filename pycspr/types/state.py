import dataclasses
import enum
import typing
from pycspr.types.cl_enums import CLAccessRights


@dataclasses.dataclass
class UnforgeableReference():
    """An unforgeable reference key.

    """
    # Access rights granted by issuer.
    access_rights: CLAccessRights

    # Uref on-chain identifier.
    address: bytes

    def as_string(self):
        """Returns a string representation for over the wire dispatch.

        """
        return f"uref-{self.address.hex()}-{self.access_rights.value:03}"


    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.access_rights == other.access_rights and \
               self.address == other.address


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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name and \
               self.key == other.key


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

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name and \
               self.key == other.key


@dataclasses.dataclass
class DictionaryIdentifier_SeedURef(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item
       via it's seed unforgeable reference.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The dictionary's seed URef.
    seed_uref: UnforgeableReference

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.seed_uref == other.seed_uref


@dataclasses.dataclass
class DictionaryIdentifier_UniqueKey(DictionaryIdentifier):
    """Encapsulates information required to query a dictionary item via it's unique key.

    """
    # The globally unique dictionary key.
    key: str

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and self.key == other.key


class KeyType(enum.Enum):
    """Enumeration over set of CL keys.

    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2


@dataclasses.dataclass
class Key():
    """A pointer to data within global state.

    """
    # 32 byte key identifier.
    identifier: bytes

    # Key type identifier.
    key_type: KeyType

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.identifier == other.identifier and \
               self.key_type == other.key_type


@dataclasses.dataclass
class List():
    """A pointer to a list of data.

    """
    # Set of associated items.
    items: typing.List[object]

    # Item type identifier.
    item_type: KeyType

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.items == other.items and \
               self.item_type == other.item_type
