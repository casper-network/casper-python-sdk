import dataclasses

from pycspr import crypto


@dataclasses.dataclass
class PublicKey:
    """Encapsulates information associated with an account's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: crypto.KeyAlgorithm

    # Public key as raw bytes.
    pbk: bytes

    @property
    def account_hash(self):
        """Returns on-chain account hash."""
        return crypto.get_account_hash(self.account_key)

    @property
    def account_key(self):
        """Returns on-chain account key."""
        return crypto.get_account_key(self.algo, self.pbk)


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
    def account_hash(self):
        """Returns on-chain account hash.

        """
        return crypto.get_account_hash(self.account_key)

    @property
    def account_key(self):
        """Returns on-chain account key.

        """
        return crypto.get_account_key(self.algo, self.pbk)

    def get_signature(self, data: bytes) -> bytes:
        """Get signature over payload.

        """
        return crypto.get_signature(data, self.pvk, self.algo)

    def as_public_key(self) -> PublicKey:
        """Returns public key representation.

        """
        return PublicKey(algo=self.algo, pbk=self.pbk)
