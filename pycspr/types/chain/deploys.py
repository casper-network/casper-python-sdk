import dataclasses
import typing

from pycspr.crypto import get_signature_for_deploy_approval
from pycspr.crypto import verify_deploy_approval_signature
from pycspr.crypto import PrivateKey
from pycspr.crypto import PublicKey
from pycspr.crypto import SignatureBytes
from pycspr.types.cl.values import CLV_Value
from pycspr.types.rpc import ContractID
from pycspr.types.rpc import ContractVersion
from pycspr.types.rpc import DeployArgument
from pycspr.types.rpc import DeployExecutableItem
from pycspr.types.rpc import DeployOfStoredContract
from pycspr.types.rpc import DeployOfStoredContractByHash
from pycspr.types.rpc import Timestamp
from pycspr.utils import constants
from pycspr.utils import conversion


@dataclasses.dataclass
class DeployApproval:
    """A digital signature approving deploy processing.

    """
    # The public key component to the signing key used to sign a deploy.
    signer: PublicKey

    # The digital signatutre signalling approval of deploy processing.
    # It's length is 65 bytes: leading byte represents ECC algo type.
    signature: SignatureBytes

    def __eq__(self, other) -> bool:
        return self.signer == other.signer and self.signature == other.signature

    @property
    def sig(self) -> bytes:
        """Returns signature denuded of leading byte (representing ECC algo)."""
        return self.signature[1:]


@dataclasses.dataclass
class DeployBody():
    """Encapsulates a deploy's body, i.e. executable payload.

    """
    # Executable information passed to chain's VM for taking
    # payment required to process session logic.
    payment: DeployExecutableItem

    # Executable information passed to chain's VM.
    session: DeployExecutableItem

    # Hash of payload.
    hash: bytes

    def __eq__(self, other) -> bool:
        return self.payment == other.payment and \
               self.session == other.session and \
               self.hash == other.hash


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
    ttl: "DeployTimeToLive"

    def __eq__(self, other) -> bool:
        return self.account_public_key == other.account_public_key and \
               self.body_hash == other.body_hash and \
               self.chain_name == other.chain_name and \
               self.dependencies == other.dependencies and \
               self.gas_price == other.gas_price and \
               self.timestamp == other.timestamp and \
               self.ttl == other.ttl


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
    ttl: "DeployTimeToLive"

    def __eq__(self, other) -> bool:
        return self.account_public_key == other.account_public_key and \
               self.chain_name == other.chain_name and \
               self.dependencies == other.dependencies and \
               self.gas_price == other.gas_price and \
               self.timestamp == other.timestamp and \
               self.ttl == other.ttl


@dataclasses.dataclass
class DeployTimeToLive():
    """Encapsulates a timeframe within which a deploy must be processed.

    """
    # TTL in milliseconds.
    as_milliseconds: int

    # Humanized representation of the ttl.
    humanized: str

    def __eq__(self, other) -> bool:
        return self.as_milliseconds == other.as_milliseconds and \
               self.humanized == other.humanized

    @staticmethod
    def from_string(as_string: str) -> "DeployTimeToLive":
        as_milliseconds = conversion.humanized_time_interval_to_milliseconds(as_string)
        if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
            raise ValueError(f"Invalid deploy ttl. Maximum (ms)={constants.DEPLOY_TTL_MS_MAX}")

        return DeployTimeToLive(
            as_milliseconds=as_milliseconds,
            humanized=as_string
        )

    @staticmethod
    def from_milliseconds(as_milliseconds: int) -> "DeployTimeToLive":
        return DeployTimeToLive(
            as_milliseconds,
            conversion.milliseconds_to_humanized_time_interval(as_milliseconds)
            )

    def to_string(self) -> str:
        return self.humanized


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
    payment: DeployExecutableItem

    # Executable information passed to chain's VM.
    session: DeployExecutableItem

    def __eq__(self, other) -> bool:
        return self.approvals == other.approvals and \
               self.hash == other.hash and \
               self.header == other.header and \
               self.payment == other.payment and \
               self.session == other.session

    def get_body(self) -> DeployBody:
        return DeployBody(
            payment=self.payment,
            session=self.session,
            hash=self.header.body_hash
        )

    def approve(self, approver: PrivateKey):
        """Creates a deploy approval & appends it to associated set.

        :params approver: Private key of entity approving the deploy.

        """
        sig = get_signature_for_deploy_approval(
            self.hash, approver.private_key, approver.key_algo
            )
        approval = DeployApproval(approver.to_public_key(), sig)
        self._append_approval(approval)

    def set_approval(self, approval: DeployApproval):
        """Appends an approval to associated set.

        :params approval: An approval to be associated with the deploy.

        """
        if not verify_deploy_approval_signature(
            self.hash,
            approval.signature,
            approval.signer.to_account_key()
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
