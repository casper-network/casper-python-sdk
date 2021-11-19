import dataclasses
import typing

from pycspr.types.cl.cl_values import CL_ByteArray
from pycspr.types.cl.cl_values import CL_String
from pycspr.types.cl.cl_values import CL_U32
from pycspr.types.deploys.deploy_argument import DeployArgument
from pycspr.types.other.identifiers import ContractIdentifer
from pycspr.types.other.identifiers import ContractVersion
from pycspr.types.other.u8_array import U8Array
from pycspr.types.other.vector import Vector


@dataclasses.dataclass
class DeployExecutableItem():
    """Encapsulates vm execution information.

    """
    # Set of arguments mapped to endpoint parameters.
    args: typing.List[DeployArgument]

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.args == other.args

    def to_bytes(self) -> bytes:
        return Vector([i.to_bytes() for i in self.args]).to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "DeployExecutableItem":
        if "ModuleBytes" in obj:
            return ModuleBytes.from_json(obj["ModuleBytes"])
        elif "StoredContractByHash" in obj:
            return StoredContractByHash.from_json(obj["StoredContractByHash"])
        elif "StoredVersionedContractByHash" in obj:
            return StoredContractByHashVersioned.from_json(obj["StoredVersionedContractByHash"])
        elif "StoredContractByName" in obj:
            return StoredContractByName.from_json(obj["StoredContractByName"])
        elif "StoredVersionedContractByName" in obj:
            return StoredContractByNameVersioned.from_json(obj["StoredVersionedContractByName"])
        elif "Transfer" in obj:
            return Transfer.from_json(obj["Transfer"])
        else:
            raise NotImplementedError("Unsupported DeployExecutableItem variant")

    #endregion


@dataclasses.dataclass
class ModuleBytes(DeployExecutableItem):
    """Encapsulates information required to execute an in-line wasm binary.

    """
    # Raw WASM payload.
    module_bytes: bytes

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.module_bytes == other.module_bytes

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "ModuleBytes":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return \
            bytes([0]) + \
            U8Array(list(self.module_bytes)).to_bytes() + \
            super().to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "ModuleBytes":
        return ModuleBytes(
            args=[DeployArgument.from_json(i) for i in obj["args"]],
            module_bytes=bytes.fromhex(obj["module_bytes"])
            )

    def to_json(self) -> dict:
        return {
            "ModuleBytes": {
                "args": [i.to_json() for i in self.args],
                "module_bytes": self.module_bytes.hex()
            }
        }

    #endregion


@dataclasses.dataclass
class StoredContract(DeployExecutableItem):
    """Encapsulates information required to execute an on-chain smart contract.

    """
    # Name of a smart contract entry point to be executed.
    entry_point: str

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.entry_point == other.entry_point

    def to_bytes(self) -> bytes:
        return CL_String(self.entry_point).to_bytes() + super().to_bytes()
    
    #endregion


@dataclasses.dataclass
class StoredContractByHash(StoredContract):
    """Encapsulates information required to execute an on-chain smart contract referenced by hash.

    """
    # On-chain smart contract address.
    hash: ContractIdentifer

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.hash == other.hash

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "StoredContractByHash":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return \
            bytes([1]) + \
            CL_ByteArray(self.hash).to_bytes() + \
            super().to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "StoredContractByHash":
        return StoredContractByHash(
            args=[DeployArgument.from_json(i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            hash=bytes.fromhex(obj["hash"])
        )

    def to_json(self) -> dict:
        return {
            "StoredContractByHash": {
                "args": [i.to_json() for i in self.args],
                "entry_point": self.entry_point,
                "hash": self.hash.hex()
            }
        }

    #endregion


@dataclasses.dataclass
class StoredContractByHashVersioned(
    StoredContractByHash
):
    """Encapsulates information required to execute a versioned on-chain smart
    contract referenced by hash.

    """
    # Smart contract version identifier.
    version: ContractVersion

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.version == other.version

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "StoredContractByHashVersioned":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return \
            bytes([2]) + \
            CL_ByteArray(self.hash).to_bytes() + \
            CL_U32(self.version).to_bytes() + \
            super().to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "StoredContractByHashVersioned":
        return StoredContractByHashVersioned(
            args=[DeployArgument.from_json(i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            hash=bytes.fromhex(obj["hash"]),
            version=obj["version"]
        )

    def to_json(self) -> dict:
        return {
            "StoredContractByHashVersioned": {
                "args": [i.to_json() for i in self.args],
                "entry_point": self.entry_point,
                "hash": self.hash.hex(),
                "version": self.version
            }
        }

    #endregion


@dataclasses.dataclass
class StoredContractByName(StoredContract):
    """Encapsulates information required to execute an on-chain
       smart contract referenced by name.

    """
    # On-chain smart contract name - in scope when dispatch & contract accounts are synonmous.
    name: str

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.name == other.name

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "StoredContractByName":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return \
            bytes([3]) + \
            CL_String(self.name).to_bytes() + \
            super().to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "StoredContractByName":
        return StoredContractByName(
            args=[DeployArgument.from_json(i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            name=obj["name"],
        )

    def to_json(self) -> dict:
        return {
            "StoredContractByName": {
                "args": [i.to_json() for i in self.args],
                "entry_point": self.entry_point,
                "version": self.version
            }
        }

    #endregion


@dataclasses.dataclass
class StoredContractByNameVersioned(
    StoredContractByName
):
    """Encapsulates information required to execute a versioned
       on-chain smart contract referenced by name.

    """
    # Smart contract version identifier.
    version: ContractVersion

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.version == other.version

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "StoredContractByNameVersioned":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return \
            bytes([4]) + \
            CL_String(self.name).to_bytes() + \
            CL_U32(self.version).to_bytes() + \
            super().to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "StoredContractByNameVersioned":
        return StoredContractByNameVersioned(
            args=[DeployArgument.from_json(i) for i in obj["args"]],
            entry_point=obj["entry_point"],
            name=obj["name"],
            version=obj["version"]
        )

    def to_json(self) -> dict:
        return {
            "StoredContractByNameVersioned": {
                "args": [i.to_json() for i in self.args],
                "entry_point": self.entry_point,
                "name": self.name,
                "version": self.version
            }
        }

    #endregion


@dataclasses.dataclass
class Transfer(DeployExecutableItem):
    """Encapsulates information required to execute a host-side balance transfer.

    """
    #region Equality & serialisation

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "StoredContractByHashVersioned":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        return bytes([5]) + super().to_bytes()

    @staticmethod
    def from_json(obj: dict) -> "StoredContractByHashVersioned":
        return Transfer(
            args=[DeployArgument.from_json(i) for i in obj["args"]],
            )

    def to_json(self) -> dict:
        return {
            "Transfer": {
                "args": [i.to_json() for i in self.args]
            }
        }

    #endregion