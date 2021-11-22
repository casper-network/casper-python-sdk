import dataclasses
import typing

from pycspr import crypto
from pycspr.types.deploys.deploy_approval import DeployApproval
from pycspr.types.deploys.deploy_executable_item import DeployExecutableItem
from pycspr.types.deploys.deploy_header import DeployHeader
from pycspr.types.other.keys import PrivateKey


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
