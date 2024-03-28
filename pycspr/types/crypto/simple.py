import enum
import typing


# Cryptographic fingerprint of data.
Digest = typing.NewType("Cryptographic fingerprint of data.", bytes)

# Cryptographic proof over a merkle trie.
MerkleProofBytes = typing.NewType("Cryptographic proof over a merkle trie.", bytes)

# Asymmetric private key associated with an account.
PrivateKeyBytes = typing.NewType("Asymmetric private key associated with an account.", bytes)

# Asymmetric public key associated with an account.
PublicKeyBytes = typing.NewType("Asymmetric public key associated with an account.", bytes)

# Cryptographic signature over data - includes single byte algo prefix.
SignatureBytes = typing.NewType("Cryptographic signature over data.", bytes)


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
