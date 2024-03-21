import dataclasses
import enum
import typing


class KeyAlgorithm(enum.Enum):
    """Enumeration over set of supported key algorithms.

    """
    ED25519 = 1
    SECP256K1 = 2


class HashAlgorithm(enum.Enum):
    """Enumeration over set of supported hash algorithms.

    """
    BLAKE2B = enum.auto()
    BLAKE3 = enum.auto()


Digest = typing.NewType("Cryptographic fingerprint of data.", bytes)


@dataclasses.dataclass
class PublicKey():
    """Encapsulates information associated with an account's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm

    # Public key as raw bytes.
    pbk: bytes

    @property
    def account_hash(self) -> bytes:
        """Returns on-chain account hash."""
        from pycspr.crypto.cl_operations import get_account_hash

        return get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Returns on-chain account key."""
        from pycspr.crypto.cl_operations import get_account_key
        
        return get_account_key(self.algo, self.pbk)

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk

    def __hash__(self) -> bytes:
        return hash(self.account_key)

    def __len__(self) -> int:
        return len(self.account_key)


@dataclasses.dataclass
class PrivateKey:
    """Encapsulates information associated with an account's private key.

    """
    # Private key as bytes - sensitive material !
    pvk: bytes

    # Public key as bytes.
    pbk: bytes

    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm = KeyAlgorithm.ED25519

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pvk == other.pvk and self.pbk == other.pbk

    def __hash__(self) -> bytes:
        return hash(self.pvk)

    def __len__(self) -> int:
        return len(self.pvk)

    @property
    def private_key(self) -> bytes:
        """Associated private key synonym."""
        return self.pvk

    @property
    def public_key(self) -> bytes:
        """Associated public key synonym."""
        return self.pbk

    @property
    def key_algo(self) -> KeyAlgorithm:
        """Associated key algorithm synonym."""
        return self.algo

    @property
    def account_hash(self) -> bytes:
        """Gets derived on-chain account hash - i.e. address."""
        from pycspr.crypto.cl_operations import get_account_hash

        return get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Gets on-chain account key."""
        from pycspr.crypto.cl_operations import get_account_key

        return get_account_key(self.algo, self.pbk)

    @property
    def as_public_key(self) -> PublicKey:
        """Returns public key representation.

        """
        return PublicKey(algo=self.algo, pbk=self.pbk)

    def get_signature(self, data: bytes) -> bytes:
        """Get signature over payload.

        """ 
        from pycspr.crypto.ecc import get_signature        
        
        return get_signature(data, self.pvk, self.algo)
