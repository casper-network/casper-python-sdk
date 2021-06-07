from pycspr.serialization.utils import CLType
from typing import Callable



# Formal type within CL type system.
TYPEOF = CLType.UNIT

# Length when encoded.
_ENCODED_LENGTH: int = 0


# Decodes input data.
decode = lambda _: None


# Encodes a domain type instance.
encode = lambda _: []


# Returns length in bytes of encoded data.
get_encoded_length = lambda _: _ENCODED_LENGTH


# A predicate returning a flag indicating whether encoded data can be decoded.
is_decodeable = lambda encoded: isinstance(encoded, list) and len(encoded) == _ENCODED_LENGTH


# A predicate returning a flag indicating whether domain type instance can be encoded.
is_encodeable = lambda v: v is None
