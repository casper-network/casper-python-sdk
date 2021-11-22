import dataclasses

from pycspr import crypto
from pycspr.types.cl_type import CL_Type_PublicKey
from pycspr.types.cl_value import CL_Value
from pycspr.types.keys import PublicKey


@dataclasses.dataclass
class CL_PublicKey(PublicKey, CL_Value):
    """Encapsulates information associated with an account's public key.

    """
    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.algo == other.algo and self.pbk == other.pbk

    def as_bytes(self) -> bytes:
        return bytes([self.algo.value]) + self.pbk

    def as_cl_type(self) -> CL_Type_PublicKey:
        return CL_Type_PublicKey()

    def as_parsed(self) -> str:
        return self.account_key.hex()

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_PublicKey":
        return CL_PublicKey(crypto.KeyAlgorithm(as_bytes[0]), as_bytes[1:])

    @staticmethod
    def from_key(as_key: PublicKey) -> "CL_PublicKey":
        return CL_PublicKey(as_key.algo, as_key.pbk)

    #endregion
