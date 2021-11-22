import dataclasses
import typing

from pycspr.types.deploys.deploy_argument import DeployArgument
from pycspr.types.other.identifiers import ContractIdentifer
from pycspr.types.other.identifiers import ContractVersion


@dataclasses.dataclass
class DeployExecutableItem():
    """Encapsulates vm execution information.

    """
    # Set of arguments mapped to endpoint parameters.
    args: typing.List[DeployArgument]

    def __eq__(self, other) -> bool:
        return self.args == other.args


@dataclasses.dataclass
class ModuleBytes(DeployExecutableItem):
    """Encapsulates information required to execute an in-line wasm binary.

    """
    # Raw WASM payload.
    module_bytes: bytes

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.module_bytes == other.module_bytes


@dataclasses.dataclass
class StoredContract(DeployExecutableItem):
    """Encapsulates information required to execute an on-chain smart contract.

    """
    # Name of a smart contract entry point to be executed.
    entry_point: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.entry_point == other.entry_point


@dataclasses.dataclass
class StoredContractByHash(StoredContract):
    """Encapsulates information required to execute an on-chain smart contract referenced by hash.

    """
    # On-chain smart contract address.
    hash: ContractIdentifer

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.hash == other.hash


@dataclasses.dataclass
class StoredContractByHashVersioned(
    StoredContractByHash
):
    """Encapsulates information required to execute a versioned on-chain smart
    contract referenced by hash.

    """
    # Smart contract version identifier.
    version: ContractVersion

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.version == other.version


@dataclasses.dataclass
class StoredContractByName(StoredContract):
    """Encapsulates information required to execute an on-chain
       smart contract referenced by name.

    """
    # On-chain smart contract name - in scope when dispatch & contract accounts are synonmous.
    name: str

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.name == other.name


@dataclasses.dataclass
class StoredContractByNameVersioned(
    StoredContractByName
):
    """Encapsulates information required to execute a versioned
       on-chain smart contract referenced by name.

    """
    # Smart contract version identifier.
    version: ContractVersion

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.version == other.version


@dataclasses.dataclass
class Transfer(DeployExecutableItem):
    """Encapsulates information required to execute a host-side balance transfer.

    """
    pass
