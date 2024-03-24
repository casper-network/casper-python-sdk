import dataclasses

from pycspr.types.crypto.simple import KeyAlgorithm


@dataclasses.dataclass
class PublicKey():
    """Encapsulates information associated with an account's public key.

    """
    # Algorithm used to generate ECC key pair.
    algo: KeyAlgorithm

    # Public key as raw bytes.
    pbk: bytes

    def to_account_hash(self) -> bytes:
        """Returns on-chain account address.

        """
        from pycspr.crypto.cl_operations import get_account_hash

        return get_account_hash(self.to_account_key())

    def to_account_key(self) -> bytes:
        """Returns on-chain account key.

        """
        # JIT import to avoid circular references.
        from pycspr.crypto.cl_operations import get_account_key

        return get_account_key(self.algo, self.pbk)

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk

    def __hash__(self) -> bytes:
        return hash(self.to_account_key())

    def __len__(self) -> int:
        return len(self.to_account_key())


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

    def to_account_hash(self) -> bytes:
        """Gets derived on-chain account hash - i.e. address.

        """
        from pycspr.crypto.cl_operations import get_account_hash

        return get_account_hash(self.to_account_key())

    def to_account_key(self) -> bytes:
        """Gets on-chain account key."""
        from pycspr.crypto.cl_operations import get_account_key

        return get_account_key(self.algo, self.pbk)

    def to_public_key(self) -> PublicKey:
        """Returns public key representation.

        """
        return PublicKey(algo=self.algo, pbk=self.pbk)

    def get_signature(self, data: bytes) -> bytes:
        """Get signature over payload.

        """
        from pycspr.crypto.ecc import get_signature

        return get_signature(data, self.pvk, self.algo)
