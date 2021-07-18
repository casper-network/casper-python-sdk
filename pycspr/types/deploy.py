import dataclasses
import datetime
import typing

from pycspr import crypto
from pycspr.types.account import AccountInfo
from pycspr.types.account import PublicKey
from pycspr.types.cl import CLValue



# On chain contract identifer.
ContractHash = typing.NewType("32 byte array emitted by a hashing algorithm representing a static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# Output of a hashing function.
Digest = typing.NewType("32 byte array emitted by a hashing algorithm", bytes)

# Output of an ECC signing function.
Signature = typing.NewType("64 byte array emitted by an ECC algorithm", bytes)

# A timestamp encodeable as millisecond precise seconds since epoch.
Timestamp = typing.NewType("POSIX timestamp", datetime.datetime)

# A human recognizable temporal delta.
HumamizedTimeDelta = typing.NewType("A temporal offset from now", str)


@dataclasses.dataclass
class ExecutionArgument():
    """An argument to be passed to vm for execution.
    
    """
    # Argument name mapped to an entry point parameter.
    name: str
    
    # Argument cl type system value. 
    value: CLValue


@dataclasses.dataclass
class ExecutableDeployItem():
    """Encapsulates vm execution information.
    
    """
    # Set of arguments mapped to endpoint parameters.
    args: typing.List[ExecutionArgument]


@dataclasses.dataclass
class ExecutableDeployItem_ModuleBytes(ExecutableDeployItem):
    """Encapsulates information required to execute an in-line wasm binary.
    
    """
    # Raw WASM payload.
    module_bytes: bytes


@dataclasses.dataclass
class ExecutableDeployItem_StoredContract(ExecutableDeployItem):
    """Encapsulates information required to execute an on-chain smart contract.
    
    """
    # Name of a smart contract entry point to be executed. 
    entry_point: str


@dataclasses.dataclass
class ExecutableDeployItem_StoredContractByHash(ExecutableDeployItem_StoredContract):
    """Encapsulates information required to execute an on-chain smart contract referenced by hash.
    
    """
    # On-chain smart contract address. 
    hash: ContractHash


@dataclasses.dataclass
class ExecutableDeployItem_StoredContractByHashVersioned(ExecutableDeployItem_StoredContractByHash):
    """Encapsulates information required to execute a versioned on-chain smart contract referenced by hash.
    
    """
    # Smart contract version identifier.
    version: ContractVersion
    

@dataclasses.dataclass
class ExecutableDeployItem_StoredContractByName(ExecutableDeployItem_StoredContract):
    """Encapsulates information required to execute an on-chain smart contract referenced by name.
    
    """
    # On-chain smart contract name - only in scope when dispatch account = contract owner account. 
    name: str


@dataclasses.dataclass
class ExecutableDeployItem_StoredContractByNameVersioned(ExecutableDeployItem_StoredContractByName):
    """Encapsulates information required to execute a versioned on-chain smart contract referenced by name.
    
    """
    # Smart contract version identifier.
    version: ContractVersion


@dataclasses.dataclass
class ExecutableDeployItem_Transfer(ExecutableDeployItem):
    """Encapsulates information required to execute a host-side balance transfer.
    
    """
    pass


@dataclasses.dataclass
class DeployApproval:
    """A digital signature approving deploy processing.
    
    """
    # The public key component to the signing key used to sign a deploy.
    signer: PublicKey

    # The digital signatutre signalling approval of deploy processing.
    signature: Signature


@dataclasses.dataclass
class DeployBody():
    """Encapsulates a deploy's body, i.e. executable payload.
    
    """
    # Executable information passed to chain's VM for taking payment required to process session logic.
    payment: ExecutableDeployItem

    # Executable information passed to chain's VM.
    session: ExecutableDeployItem

    # Hash of payload.
    hash: Digest


@dataclasses.dataclass
class DeployTimeToLive():
    """Encapsulates a timeframe within which a deploy must be processed.
    
    """
    # TTL in milliseconds.
    as_milliseconds: int

    # Humanized representation of the ttl.
    humanized: str


@dataclasses.dataclass
class DeployHeader():
    """Encapsulates header information associated with a deploy.
    
    """
    # Public key of account dispatching deploy to a node.
    accountPublicKey: PublicKey

    # Hash of deploy payload.
    body_hash: Digest

    # Name of target chain to which deploy will be dispatched.
    chain_name: str

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[Digest]

    # Multiplier in motes used to calculate final gas price.
    gas_price: int

    # Timestamp at point of deploy creation.
    timestamp: Timestamp

    # Time interval after which the deploy will no longer be considered for processing by a node.
    ttl: DeployTimeToLive


@dataclasses.dataclass
class Deploy():
    """Top level container encapsulating information required to interact with chain.
    
    """
    # Set of signatures approving this deploy for execution.
    approvals: typing.List[DeployApproval]

    # Unique identifier.
    hash: Digest

    # Header information encapsulating various information impacting deploy processing.
    header: DeployHeader

    # Executable information passed to chain's VM for taking payment required to process session logic.
    payment: ExecutableDeployItem

    # Executable information passed to chain's VM.
    session: ExecutableDeployItem


    def set_approval(self, account: AccountInfo):
        """Appends an approval to associated set.
        
        """
        self.approvals.append(
            DeployApproval(
                signer=account.account_key, 
                signature=crypto.get_signature(
                    self.hash,
                    account.private_key,
                    algo=account.algo
                    )
                )
            )
    
        # Remove potential duplicates.
        uniques = set()
        self.approvals = [uniques.add(a.signer) or a for a in self.approvals if a.signer not in uniques]


@dataclasses.dataclass
class DeployParameters():
    """Encapsulates standard information associated with a deploy.
    
    """
    # Public key of account dispatching deploy to a node.
    accountPublicKey: PublicKey

    # Name of target chain to which deploy will be dispatched.
    chain_name: str

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[Digest]

    # Multiplier in motes used to calculate final gas price.
    gas_price: int

    # Timestamp at point of deploy creation.
    timestamp: Timestamp

    # Time interval in milliseconds after which the deploy will no longer be considered for processing by a node.
    ttl: HumamizedTimeDelta
