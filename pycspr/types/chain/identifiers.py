import dataclasses
import datetime as dt
import enum
import typing

from pycspr.types.cl.values import CLV_URef

from pycspr.crypto.types import Digest
from pycspr.crypto.types import PublicKeyBytes
from pycspr.types.rpc import AccountID
from pycspr.types.rpc import BlockID
from pycspr.types.rpc import DeployHash
from pycspr.types.rpc import StateRootHash


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
