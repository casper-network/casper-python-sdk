import dataclasses
import enum
import typing


# Cryptographic fingerprint of data.
DigestBytes = typing.NewType(
    "Cryptographic fingerprint of data.", bytes
    )

# Hexadecimal encoded crryptographic fingerprint of data.
DigestHex = typing.NewType(
    "Cryptographic fingerprint of data.", bytes
    )

# Cryptographic proof over a merkle trie.
MerkleProofBytes = typing.NewType(
    "Cryptographic proof over a merkle trie.", bytes
    )

# Hexadecimal encoded cryptographic proof over a merkle trie.
MerkleProofHex = typing.NewType(
    "Hexadecimal encoded cryptographic proof over a merkle trie.", bytes
    )

# Asymmetric private key associated with an account.
PrivateKeyBytes = typing.NewType(
    "Asymmetric private key associated with an account.", bytes
    )

# Hexadecimal encoded asymmetric private key associated with an account.
PrivateKeyHex = typing.NewType(
    "Hexadecimal encoded asymmetric private key associated with an account.", str
    )

# PEM encoded asymmetric private key associated with an account.
PrivateKeyPem = typing.NewType(
    "PEM encoded asymmetric private key associated with an account.", bytes
    )

# Asymmetric public key associated with an account.
PublicKeyBytes = typing.NewType(
    "Asymmetric public key associated with an account.", bytes
    )

# Hexadecimal encoded asymmetric public key associated with an account.
PublicKeyHex = typing.NewType(
    "Hexadecimal encoded asymmetric public key associated with an account.", str
    )

# Cryptographic signature over data - includes single byte algo prefix.
SignatureBytes = typing.NewType(
    "Cryptographic signature over data.", bytes
    )

# Hexadecimal encoded cryptographic signature over data - includes single byte algo prefix.
SignatureHex = typing.NewType(
    "Hexadecimal encoded cryptographic signature over data.", bytes
    )


class HashAlgorithm(enum.Enum):
    """Enumeration over set of supported hash algorithms.

    """
    BLAKE2B = enum.auto()
    BLAKE3 = enum.auto()


class KeyAlgorithm(enum.Enum):
    """Enumeration over set of supported key algorithms.

    """
    ED25519 = 1
    SECP256K1 = 2


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
    DigestBytes,
    DigestHex,
    MerkleProofBytes,
    MerkleProofHex,
    PrivateKeyBytes,
    PrivateKeyHex,
    PublicKeyBytes,
    PublicKeyHex,
    SignatureBytes,
    SignatureHex,
} | {
    HashAlgorithm,
    KeyAlgorithm,
} | {
    PublicKey,
    PrivateKey,
    Signature,
}
