from pycspr.serialization.utils import int_to_le_bytes



# Length when encoded.
_ENCODED_LENGTH: int = 4

# Dimension constraints.
MIN_SIZE = 0
MAX_SIZE = (2 ** 32) - 1


# Encodes parsed data.
encode = lambda v: int_to_le_bytes(int(v), _ENCODED_LENGTH, False)
