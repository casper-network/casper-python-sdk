import dataclasses
import typing

from pycspr import crypto
from pycspr.types.deploy_approval import DeployApproval
from pycspr.types.deploy_executable_item import DeployExecutableItem
from pycspr.types.deploy_header import DeployHeader
from pycspr.types.keys import PrivateKey


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

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.approvals == other.approvals and \
               self.hash == other.hash and \
               self.header == other.header and \
               self.payment == other.payment and \
               self.session == other.session

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "Deploy":
        raise NotImplementedError()

    def to_bytes(self) -> bytes:
        raise NotImplementedError()

    @staticmethod
    def from_json(obj: dict) -> "Deploy":
        return Deploy(
            approvals=[DeployApproval.from_json(i) for i in obj["approvals"]],
            hash=bytes.fromhex(obj["hash"]),
            header=DeployHeader.from_json(obj["header"]),
            payment=DeployExecutableItem.from_json(obj["payment"]),
            session=DeployExecutableItem.from_json(obj["session"])
        )

    def to_json(self) -> dict:
        return {
            "approvals": [i.to_json(i) for i in self.approvals],
            "hash": self.hash.hex(),
            "header": self.header.to_json(),
            "payment": self.payment.to_json(),
            "session": self.session.to_json()
        }

    #endregion
