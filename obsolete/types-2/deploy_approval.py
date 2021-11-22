import  dataclasses

from pycspr.types.keys import PublicKey


@dataclasses.dataclass
class DeployApproval:
    """A digital signature approving deploy processing.

    """
    # The public key component to the signing key used to sign a deploy.
    signer: PublicKey

    # The digital signatutre signalling approval of deploy processing.
    signature: bytes

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.signer == other.signer and \
               self.signature == other.signature

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "DeployApproval":
        raise NotImplementedError()


    @staticmethod
    def from_json(obj: dict) -> "DeployApproval":
        return DeployApproval(
            signer=PublicKey.from_json(obj["signer"]),
            signature=bytes.fromhex(obj["signature"]),
        )


    def to_bytes(self) -> bytes:
        return self.signer + self.signature


    def to_json(self) -> dict:
        return {
            "signature": self.signature.hex(),
            "signer": self.signer.hex()
        }

    #endregion
