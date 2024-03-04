import dataclasses
import enum
import typing

from pycspr.types.cl_values import CL_URef


# The output of a one way hashing function - 32 bytes.
Digest = typing.Union[bytes, str]

# An account identifier may be a byte array of 33 bytes,
# a hexadecimal string of 66 characters.
AccountID = typing.Union[bytes, str]

# A block identifier: byte array | hex string | height,
BlockID = typing.Union[Digest, int]

# On chain contract identifier.
ContractID = typing.NewType("Static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# A deploy identifier is a 32 byte array or it's hexadecimal string equivalent.
DeployID = typing.Union[bytes, str]

# A public key associated with an assymetric key pair controlled by an entity.
PublicKey = typing.Union[bytes, str]

# Root id of a node's global state.
StateRootID = typing.Union[bytes, str]


@dataclasses.dataclass
class PurseID():
    # Purse identifier - account id | public key | uref.
    identifier: typing.Union[AccountID, PublicKey, CL_URef]

    # Type of identifier.
    id_type: "PurseIDType"


class PurseIDType(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    PUBLIC_KEY = enum.auto()
    ACCOUNT_HASH = enum.auto()
    UREF = enum.auto()


@dataclasses.dataclass
class GlobalStateID():
    # 32 byte global state identifier, either a block hash, block height or state root hash.
    identifier: typing.Union[bytes, str, int]

    # Type of identifier.
    id_type: "GlobalStateIDType"


class GlobalStateIDType(enum.Enum):
    """Enumeration over set of CL type keys.

    """
    BLOCK_HASH = enum.auto()
    BLOCK_HEIGHT = enum.auto()
    STATE_ROOT_HASH = enum.auto()


@dataclasses.dataclass
class DictionaryID():
    """A set of variants for performation dictionary item state queries.

    """
    pass


@dataclasses.dataclass
class DictionaryID_AccountNamedKey(DictionaryID):
    """Encapsulates information required to query a dictionary item via an Account's named keys.

    """
    # The account key as a formatted string whose named keys contains dictionary_name.
    account_key: str

    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.account_key == other.account_key and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name


@dataclasses.dataclass
class DictionaryID_ContractNamedKey(DictionaryID):
    """Encapsulates information required to query a dictionary item via a Contract's named keys.

    """
    # The contract key as a formatted string whose named keys contains dictionary_name.
    contract_key: str

    # The dictionary item key.
    dictionary_item_key: str

    # The named key under which the dictionary seed URef is stored.
    dictionary_name: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.contract_key == other.contract_key and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.dictionary_name == other.dictionary_name


@dataclasses.dataclass
class DictionaryID_SeedURef(DictionaryID):
    """Encapsulates information required to query a dictionary item
       via it's seed unforgeable reference.

    """
    # The dictionary item key.
    dictionary_item_key: str

    # The dictionary's seed URef.
    seed_uref: object

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.dictionary_item_key == other.dictionary_item_key and \
               self.seed_uref == other.seed_uref


@dataclasses.dataclass
class DictionaryID_UniqueKey(DictionaryID):
    """Encapsulates information required to query a dictionary item via it's unique key.

    """
    # The globally unique dictionary key.
    key: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.key == other.key
