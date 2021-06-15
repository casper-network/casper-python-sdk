import dataclasses
import datetime
import typing

from pycspr.types.cl import CLType
from pycspr.types.cl import CLValue


# Name of target chain to which deploys may be dispatched.
ChainName = typing.NewType("Simple chain identifer", str)

# On chain contract identifer.
ContractHash = typing.NewType("32 byte array emitted by a hashing algorithm representing a static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# A public key derived from an ECC key pair.
PublicKey = typing.NewType("Either 32 or 33 bytes (compressed) depending upon ECC type", bytes)

# Output of a hashing function.
Digest = typing.NewType("32 byte array emitted by a hashing algorithm", bytes)

# Output of an ECC signing function.
Signature = typing.NewType("64 byte array emitted by an ECC algorithm", bytes)

# A timestamp encodeable as millisecond precise seconds since epoch.
Timestamp = typing.NewType("POSIX timestamp", datetime.datetime)

# A human recognizable temporal delta.
HumamizedTimeDelta = typing.NewType("A temporal offset from now", str)


@dataclasses.dataclass
class Approval:
    """A digital signature approving deploy processing.
    
    """
    # The public key component to the signing key used to sign a deploy.
    signer: PublicKey

    # The digital signatutre signalling approval of deploy processing.
    signature: Signature


@dataclasses.dataclass
class ExecutionArgument():
    """An argument to be passed to vm for execution.
    
    """
    # Argument name mapped to an entry point parameter.
    name: str
    
    # Argument cl type system value. 
    value: CLValue


@dataclasses.dataclass
class ExecutionInfo():
    """Encapsulates vm execution information.
    
    """
    # Set of arguments mapped to endpoint parameters.
    args: typing.List[ExecutionArgument]


@dataclasses.dataclass
class ExecutionInfo_ModuleBytes(ExecutionInfo):
    """Encapsulates information required to execute an in-line wasm binary.
    
    """
    # Raw WASM payload.
    module_bytes: bytes


@dataclasses.dataclass
class ExecutionInfo_StoredContract(ExecutionInfo):
    """Encapsulates information required to execute an on-chain smart contract.
    
    """
    # Name of a smart contract entry point to be executed. 
    entry_point: str


@dataclasses.dataclass
class ExecutionInfo_StoredContractByHash(ExecutionInfo_StoredContract):
    """Encapsulates information required to execute an on-chain smart contract referenced by hash.
    
    """
    # On-chain smart contract address. 
    hash: ContractHash


@dataclasses.dataclass
class ExecutionInfo_StoredContractByHashVersioned(ExecutionInfo_StoredContractByHash):
    """Encapsulates information required to execute a versioned on-chain smart contract referenced by hash.
    
    """
    # Smart contract version identifier.
    version: ContractVersion
    

@dataclasses.dataclass
class ExecutionInfo_StoredContractByName(ExecutionInfo_StoredContract):
    """Encapsulates information required to execute an on-chain smart contract referenced by name.
    
    """
    # On-chain smart contract name - only in scope when dispatch account = contract owner account. 
    name: str


@dataclasses.dataclass
class ExecutionInfo_StoredContractByNameVersioned(ExecutionInfo_StoredContractByName):
    """Encapsulates information required to execute a versioned on-chain smart contract referenced by name.
    
    """
    # Smart contract version identifier.
    version: ContractVersion


@dataclasses.dataclass
class ExecutionInfo_Transfer(ExecutionInfo):
    """Encapsulates information required to execute a host-side balance transfer.
    
    """
    pass


@dataclasses.dataclass
class DeployBody():
    """Encapsulates a deploy's body, i.e. executable payload.
    
    """
    # Executable information passed to chain's VM for taking payment required to process session logic.
    payment: ExecutionInfo

    # Executable information passed to chain's VM.
    session: ExecutionInfo

    @property
    def hash(self) -> bytes:
        """Derives deploy hash based upon header attributes + body hash.
        
        """
        # TODO: calculate hash base upon session.to_bytes + payment.to_bytes
        return bytes.fromhex("44682ea86b704fb3c65cd16f84a76b621e04bbdb3746280f25cf062220e471b4")


@dataclasses.dataclass
class DeployHeader():
    """Encapsulates header information associated with a deploy.
    
    """
    # Public key of account dispatching deploy to a node.
    account: PublicKey

    # Hash of deploy payload.
    body_hash: Digest

    # Name of target chain to which deploy will be dispatched.
    chain_name: ChainName

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[Digest]

    # Multiplier in motes used to calculate final gas price.
    gas_price: int

    # Timestamp at point of deploy creation.
    timestamp: Timestamp

    # Time interval after which the deploy will no longer be considered for processing by a node.
    ttl: HumamizedTimeDelta

    @property
    def hash(self) -> bytes:
        """Derives deploy hash based upon header attributes + body hash.
        
        """
        # TODO: calculate hash based upon attributes + body-hash.
        return bytes.fromhex("44682ea86b704fb3c65cd16f84a76b621e04bbdb3746280f25cf062220e471b4")


@dataclasses.dataclass
class Deploy():
    """Top level container encapsulating information required to interact with chain.
    
    """
    # Set of signatures approving this deploy for execution.
    approvals: typing.List[Approval]

    # Unique identifier.
    hash: Digest

    # Header information encapsulating various information impacting deploy processing.
    header: DeployHeader

    # Executable information passed to chain's VM for taking payment required to process session logic.
    payment: ExecutionInfo

    # Executable information passed to chain's VM.
    session: ExecutionInfo


@dataclasses.dataclass
class StandardParameters():
    """Encapsulates standard information associated with a deploy.
    
    """
    # Public key of account dispatching deploy to a node.
    account: PublicKey

    # Name of target chain to which deploy will be dispatched.
    chain_name: ChainName

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[Digest]

    # Multiplier in motes used to calculate final gas price.
    gas_price: int

    # Timestamp at point of deploy creation.
    timestamp: Timestamp

    # Time interval after which the deploy will no longer be considered for processing by a node.
    ttl: HumamizedTimeDelta
