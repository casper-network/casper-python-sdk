import dataclasses
import enum
import typing

from pycspr.types.cl.values import CLV_URef
from pycspr.types.crypto import Digest
from pycspr.types.crypto import PublicKeyBytes


Address = typing.NewType("Identifier of an on-chain account address.", bytes)

AccountID = typing.NewType("Identifier of an on-chain account.", Address)

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
    BLOCK_HASH = enum.auto()
    BLOCK_HEIGHT = enum.auto()
    STATE_ROOT_HASH = enum.auto()


@dataclasses.dataclass
class PurseID():
    identifier: typing.Union[AccountID, PublicKeyBytes, CLV_URef]
    id_type: "PurseIDType"


class PurseIDType(enum.Enum):
    PUBLIC_KEY = enum.auto()
    ACCOUNT_HASH = enum.auto()
    UREF = enum.auto()
