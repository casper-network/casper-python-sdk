import dataclasses

from pycspr import crypto
from pycspr.types.cl_types import CL_Type_PublicKey
from pycspr.types.cl_values.base import CL_Value
from pycspr.types.other import PublicKey


@dataclasses.dataclass
class CL_PublicKey(PublicKey, CL_Value):
    """Encapsulates information associated with an account's public key.

    """
    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk

    @staticmethod
    def from_key(as_key: PublicKey) -> "CL_PublicKey":
        return CL_PublicKey(as_key.algo, as_key.pbk)
