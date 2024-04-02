import dataclasses
import enum
import typing

from pycspr.types.crypto import Digest
from pycspr.types.crypto import PublicKeyBytes


AccountKey = typing.NewType("On-chain account public key prefixed with ecc algo type.", bytes)

Address = typing.NewType("Identifier of an on-chain account address.", bytes)

BlockHash = typing.NewType("Digest over a block.", Digest)

BlockHeight = typing.NewType(
    "A specific location in a blockchain, measured by how many finalised blocks precede it.",
    int
)

BlockID = typing.Union[BlockHash, BlockHeight]

ContractID = typing.NewType("Identifier of an on-chain smart contract.", bytes)

ContractVersion = typing.NewType("Version of an on-chain smart contract.", int)

DeployHash = typing.NewType("Identifier of a transaction.", Digest)

EraID = typing.NewType("Identifier of an era in chain time.", int)

Gas = typing.NewType("Atomic unit of constraint over node compute.", int)

GasPrice = typing.NewType("Price of gas within an era in chain time.", int)

Motes = typing.NewType("Basic unit of crypto economic system.", int)

WasmModule = typing.NewType("WASM module payload.", bytes)

Weight = typing.NewType("Some form of relative relevance measure.", int)

StateRootHash = typing.NewType("Root digest of a node's global state.", Digest)


@dataclasses.dataclass
class GlobalStateID():
    identifier: typing.Union[BlockHash, BlockHeight, StateRootHash]
    id_type: "GlobalStateIDType"


class GlobalStateIDType(enum.Enum):
    BLOCK_HASH = "BlockHash"
    BLOCK_HEIGHT = "BlockHeight"
    STATE_ROOT_HASH = "StateRootHash"


@dataclasses.dataclass
class PurseID():
    identifier: typing.Union[Address, PublicKeyBytes, "URef"]
    id_type: "PurseIDType"


class PurseIDType(enum.Enum):
    PUBLIC_KEY = enum.auto()
    ACCOUNT_HASH = enum.auto()
    UREF = enum.auto()


class ReactorState(enum.Enum):
    INITIALIZE = "Initialize"
    CATCH_UP = "CatchUp"
    UPGRADING = "Upgrading"
    KEEP_UP = "KeepUp"
    VALIDATE = "Validate"
    SHUTDOWN_FOR_UPGRADE = "ShutdownForUpgrade"


class URefAccessRights(enum.Enum):
    NONE = 0
    READ = 1
    WRITE = 2
    ADD = 4
    READ_WRITE = 3
    READ_ADD = 5
    ADD_WRITE = 6
    READ_ADD_WRITE = 7


class ValidatorStatusChangeType(enum.Enum):
    ADDED = "Added"
    REMOVED = "Removed"
    BANNED = "Banned"
    CANNOT_PROPOSE = "CannotPropose"
    SEEN_AS_FAULTY = "SeenAsFaulty"
