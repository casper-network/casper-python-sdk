import dataclasses
import datetime
import enum
import typing
from pycspr.types.cl_enums import CLAccessRights
from pycspr.types.cl_type import CLType


# An account identifier may be a byte array of 33 bytes,
# a hexadecimal string of 66 characters.
AccountIdentifer = typing.Union[bytes, str]

# A block identifier may be a byte array of 32 bytes,
# a hexadecimal string of 64 characters or a positive integer.
BlockIdentifer = typing.Union[bytes, str, int]

# On chain contract identifier.
ContractIdentifer = typing.NewType("Static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# A deploy identifier is a 32 byte array or it's hexadecimal string equivalent.
DeployIdentifer = typing.Union[bytes, str]


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
    seed_uref: lambda: UnforgeableReference

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


@dataclasses.dataclass
class List():
    """A pointer to a list of data.

    """
    # Set of associated items.
    items: typing.List[object]

    # Item type identifier.
    item_type: CLType

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.items == other.items and \
               self.item_type == other.item_type


class StateKeyType(enum.Enum):
    """Enumeration over set of global state key types.

    """
    ACCOUNT = 0
    HASH = 1
    UREF = 2


@dataclasses.dataclass
class StateKey():
    """A pointer to data within global state.

    """
    # 32 byte key identifier.
    identifier: bytes

    # Key type identifier.
    key_type: StateKeyType

    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.identifier == other.identifier and \
               self.key_type == other.key_type


# Root hash of a node's global state.
StateRootIdentifier = typing.NewType(
    "Cumulative hash of block execution effects over global state.",
    bytes
    )

# A timestamp encodeable as millisecond precise seconds since epoch.
Timestamp = typing.NewType("POSIX timestamp", datetime.datetime)

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
