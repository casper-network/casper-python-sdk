import dataclasses
import enum
import typing

from pycspr.api.node.bin.types.crypto.simple import \
    KeyAlgorithm, \
    PrivateKeyBytes, \
    PublicKeyBytes, \
    SignatureBytes


@dataclasses.dataclass
class PublicKey():
    """Encapsulates information associated with an account's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm

    # Public key as raw bytes.
    pbk: PublicKeyBytes

    def __eq__(self, other: "PublicKey") -> bool:
        if isinstance(other, PublicKey):
            return self.algo == other.algo and self.pbk == other.pbk
        else:
            return False

    def __hash__(self) -> int:
        return hash(self.pbk)

    def __len__(self) -> int:
        return len(self.pbk) + 1

    def __str__(self) -> str:
        return f"{self.algo.name}::{self.pbk.hex()}"


@dataclasses.dataclass
class PrivateKey:
    """Encapsulates information associated with an account's private key.

    """
    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm

    # Private key as bytes - sensitive material !
    pvk: PrivateKeyBytes

    # Public key as bytes.
    pbk: PublicKeyBytes

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pvk == other.pvk and self.pbk == other.pbk

    def __hash__(self) -> int:
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

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.sig == other.sig

    def __hash__(self) -> int:
        return hash(self.sig)

    def __len__(self) -> int:
        return len(self.sig) + 1
