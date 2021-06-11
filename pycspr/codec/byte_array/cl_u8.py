from pycspr.serialization.utils import int_to_le_bytes



# Length when encoded.
_ENCODED_LENGTH: int = 1


# Encodes parsed data.
encode = lambda v: int_to_le_bytes(int(v), _ENCODED_LENGTH, False)
