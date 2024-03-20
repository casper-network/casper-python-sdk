import dataclasses

from pycspr import crypto


@dataclasses.dataclass
class PublicKey():
    """Encapsulates information associated with an account's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: crypto.KeyAlgorithm

    # Public key as raw bytes.
    pbk: bytes

    @property
    def account_hash(self) -> bytes:
        """Returns on-chain account hash."""
        return crypto.get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Returns on-chain account key."""
        return crypto.get_account_key(self.algo, self.pbk)

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
    algo: crypto.KeyAlgorithm = crypto.KeyAlgorithm.ED25519

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
    def key_algo(self) -> crypto.KeyAlgorithm:
        """Associated key algorithm synonym."""
        return self.algo

    @property
    def account_hash(self) -> bytes:
        """Gets derived on-chain account hash - i.e. address."""
        return crypto.get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Gets on-chain account key."""
        return crypto.get_account_key(self.algo, self.pbk)

    @property
    def as_public_key(self) -> PublicKey:
        """Returns public key representation.

        """
        return PublicKey(algo=self.algo, pbk=self.pbk)

    def get_signature(self, data: bytes) -> bytes:
        """Get signature over payload.

        """
        return crypto.get_signature(data, self.pvk, self.algo)
