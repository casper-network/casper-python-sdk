import enum



class KeyAlgorithm(enum.Enum):
    """Enumeration over set of supported key algorithms.
    
    """
    ED25519 = enum.auto()
    SECP256K1 = enum.auto()


class KeyEncoding(enum.Enum):
    """Enumeration over set of supported key encodings.
    
    """
    BYTES = enum.auto()
    HEX = enum.auto()
    PEM = enum.auto()


class SignatureEncoding(enum.Enum):
    """Enumeration over set of supported signature encodings.
    
    """
    BYTES = enum.auto()
    HEX = enum.auto()


class HashAlgorithm(enum.Enum):
    """Enumeration over set of supported hash algorithms.
    
    """
    BLAKE2B = enum.auto()


class HashEncoding(enum.Enum):
    """Enumeration over set of supported hash encodings.
    
    """
    BYTES = enum.auto()
    HEX = enum.auto()
