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
}
