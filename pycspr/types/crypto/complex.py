import dataclasses

from pycspr.types.crypto.simple import KeyAlgorithm
from pycspr.types.crypto.simple import PrivateKeyBytes
from pycspr.types.crypto.simple import PublicKeyBytes
from pycspr.types.crypto.simple import SignatureBytes


@dataclasses.dataclass
class PublicKey():
    """Encapsulates information associated with an account's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm

    # Public key as raw bytes.
    pbk: PublicKeyBytes

    @property
    def account_key(self) -> bytes:
        return bytes([self.algo.value]) + self.pbk

    @property
    def as_bytes(self) -> bytes:
        return bytes([self.algo.value]) + self.pbk

    def to_account_hash(self) -> bytes:
        """Returns on-chain account address.

        """
        from pycspr.crypto.cl_operations import get_account_hash

        return get_account_hash(self.account_key)

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk

    def __hash__(self) -> bytes:
        return hash(self.account_key)

    def __len__(self) -> int:
        return len(self.pbk) + 1
    
    @staticmethod
    def from_bytes(account_key: bytes) -> "PublicKey":
        return PublicKey(KeyAlgorithm(account_key[0]), account_key[1:])


@dataclasses.dataclass
class PrivateKey:
    """Encapsulates information associated with an account's private key.

    """
    # Private key as bytes - sensitive material !
    pvk: PrivateKeyBytes

    # Public key as bytes.
    pbk: PublicKeyBytes

    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm = KeyAlgorithm.ED25519

    @property
    def account_key(self) -> bytes:
        return bytes([self.algo.value]) + self.pbk

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pvk == other.pvk and self.pbk == other.pbk

    def __hash__(self) -> bytes:
        return hash(self.pvk)

    def __len__(self) -> int:
        return len(self.pvk)

    def to_public_key(self) -> PublicKey:
        """Returns public key representation.

        """
        return PublicKey(algo=self.algo, pbk=self.pbk)


@dataclasses.dataclass
class Signature():
    """Encapsulates information associated with a signature over some data.

    """
    # Associated ECC algorithm.
    algo: KeyAlgorithm

    # Signature as raw bytes.
    sig: SignatureBytes

    @property
    def to_bytes(self) -> bytes:
        return bytes([self.algo.value]) + self.sig

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.sig == other.sig

    def __hash__(self) -> bytes:
        return hash(self.sig)

    def __len__(self) -> int:
        return len(self.sig) + 1

    @staticmethod
    def from_bytes(encoded: bytes) -> "Signature":
        return Signature(
            algo=KeyAlgorithm(encoded[0]),
            sig=encoded[1:]
            )


TYPESET: set = {
    PublicKey,
    PrivateKey,
    Signature,
}
