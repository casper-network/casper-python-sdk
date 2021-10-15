import enum


class KeyAlgorithm(enum.Enum):
    """Enumeration over set of supported key algorithms.

    """
    ED25519 = 1
    SECP256K1 = 2


class HashAlgorithm(enum.Enum):
    """Enumeration over set of supported hash algorithms.

    """
    BLAKE2B = enum.auto()
