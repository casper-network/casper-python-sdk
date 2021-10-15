import dataclasses
import datetime
import typing

from pycspr import crypto
from pycspr.types.account import PrivateKey
from pycspr.types.account import PublicKey
from pycspr.types.cl import CLValue


# On chain contract identifier.
ContractHash = typing.NewType("Static contract pointer", bytes)

# On chain contract version.
ContractVersion = typing.NewType("U32 integer representing", int)

# A timestamp encodeable as millisecond precise seconds since epoch.
Timestamp = typing.NewType("POSIX timestamp", datetime.datetime)


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
class ExecutableDeployItem_StoredContractByHashVersioned(
    ExecutableDeployItem_StoredContractByHash
):
    """Encapsulates information required to execute a versioned on-chain smart
    contract referenced by hash.

    """
    # Smart contract version identifier.
    version: ContractVersion


@dataclasses.dataclass
class ExecutableDeployItem_StoredContractByName(ExecutableDeployItem_StoredContract):
    """Encapsulates information required to execute an on-chain
       smart contract referenced by name.

    """
    # On-chain smart contract name - in scope when dispatch & contract accounts are synonmous.
    name: str


@dataclasses.dataclass
class ExecutableDeployItem_StoredContractByNameVersioned(
    ExecutableDeployItem_StoredContractByName
):
    """Encapsulates information required to execute a versioned
       on-chain smart contract referenced by name.

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
    signature: bytes


@dataclasses.dataclass
class DeployBody():
    """Encapsulates a deploy's body, i.e. executable payload.

    """
    # Executable information passed to chain's VM for taking
    # payment required to process session logic.
    payment: ExecutableDeployItem

    # Executable information passed to chain's VM.
    session: ExecutableDeployItem

    # Hash of payload.
    hash: bytes


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
    account_public_key: PublicKey

    # Hash of deploy payload.
    body_hash: bytes

    # Name of target chain to which deploy will be dispatched.
    chain_name: str

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[bytes]

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
    hash: bytes

    # Header information encapsulating various information impacting deploy processing.
    header: DeployHeader

    # Executable information passed to chain's VM for taking
    # payment required to process session logic.
    payment: ExecutableDeployItem

    # Executable information passed to chain's VM.
    session: ExecutableDeployItem

    def approve(self, approver: PrivateKey):
        """Creates a deploy approval & appends it to associated set.

        :params approver: Private key of entity approving the deploy.

        """
        sig = crypto.get_signature_for_deploy_approval(
            self.hash, approver.private_key, approver.key_algo
            )
        self._append_approval(DeployApproval(approver.account_key, sig))


    def set_approval(self, approval: DeployApproval):
        """Appends an approval to associated set.

        :params approval: An approval to be associated with the deploy.

        """
        if not crypto.verify_deploy_approval_signature(
            self.hash, approval.signature, approval.signer
        ):
            raise ValueError("Invalid signature - please review your processes.")

        self._append_approval(approval)


    def _append_approval(self, approval: DeployApproval):
        """Appends an approval to managed set - implicitly deduplicating.

        """
        self.approvals.append(approval)
        uniques = set()
        self.approvals = [
            uniques.add(a.signer) or a for a in self.approvals if a.signer not in uniques
            ]


@dataclasses.dataclass
class DeployParameters():
    """Encapsulates standard information associated with a deploy.

    """
    # Public key of account dispatching deploy to a node.
    account_public_key: PublicKey

    # Name of target chain to which deploy will be dispatched.
    chain_name: str

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[bytes]

    # Multiplier in motes used to calculate final gas price.
    gas_price: int

    # Timestamp at point of deploy creation.
    timestamp: Timestamp

    # Time interval in milliseconds after which the deploy will no processed by a node.
    ttl: DeployTimeToLive
