import dataclasses

from pycspr.types.deploys.deploy_executable_item import DeployExecutableItem


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
