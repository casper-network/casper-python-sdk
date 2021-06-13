from pycspr.types.cl import CLTypeKey
from pycspr.serialization.utils import int_from_le_bytes
from pycspr.serialization.utils import int_to_le_bytes



# Formal type within CL type system.
TYPEOF = CLTypeKey.U256

# Length when encoded.
_ENCODED_LENGTH: int = 32

# Dimension constraint.
_MIN = 0
_MAX = (2 ** 256) - 1


# Decodes input data.
decode = lambda v: int_from_le_bytes(v, False)


# Encodes a domain type instance.
encode = lambda v: int_to_le_bytes(v, _ENCODED_LENGTH, False)


# Returns length in bytes of encoded data.
get_encoded_length = lambda _: _ENCODED_LENGTH


# A predicate returning a flag indicating whether encoded data can be decoded.
is_decodeable = lambda encoded: isinstance(encoded, list) and len(encoded) == _ENCODED_LENGTH


# A predicate returning a flag indicating whether domain type instance can be encoded.
is_encodeable = lambda v: isinstance(v, int) and _MIN <= v <= _MAX
