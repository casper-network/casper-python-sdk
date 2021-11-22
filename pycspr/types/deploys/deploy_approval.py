import dataclasses

from pycspr.types.other.keys import PublicKey


@dataclasses.dataclass
class DeployApproval:
    """A digital signature approving deploy processing.

    """
    # The public key component to the signing key used to sign a deploy.
    signer: PublicKey

    # The digital signatutre signalling approval of deploy processing.
    signature: bytes

    def __eq__(self, other) -> bool:
        return self.signer == other.signer and self.signature == other.signature
