import typing


# Cryptographic fingerprint of data.
DigestBytes = typing.NewType(
    "32 byte cryptographic fingerprint over data.", bytes
    )

# Hexadecimal encoded crryptographic fingerprint of data.
DigestHex = typing.NewType(
    "64 char cryptographic fingerprint of data.", str
    )

# Cryptographic proof over a merkle trie.
MerkleProofBytes = typing.NewType(
    "Cryptographic proof over a merkle trie.", bytes
    )

# Hexadecimal encoded cryptographic proof over a merkle trie.
MerkleProofHex = typing.NewType(
    "Hexadecimal encoded cryptographic proof over a merkle trie.", str
    )

# Base64 encoded asymmetric private key associated with an account.
PrivateKeyBase64 = typing.NewType(
    "Base64 encoded asymmetric private key associated with an account.", str
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
    "Hexadecimal encoded cryptographic signature over data.", str
    )
