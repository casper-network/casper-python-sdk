import enum



class KeyAlgorithm(enum.Enum):
    """Enumeration over set of supported key algorithms.
    
    """
    ED25519 = enum.auto()
    SECP256K1 = enum.auto()


class HashAlgorithm(enum.Enum):
    """Enumeration over set of supported hash algorithms.
    
    """
    BLAKE2B = enum.auto()
