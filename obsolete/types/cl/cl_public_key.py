import dataclasses

from pycspr import crypto
from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_PublicKey(CL_Value):
    # Algorithm used to generate ECC key pair.
    algo: crypto.KeyAlgorithm

    # Public key as raw bytes.
    pbk: bytes

    @property
    def account_hash(self) -> bytes:
        """Returns on-chain account hash."""
        return crypto.get_account_hash(self.account_key)

    @property
    def account_key(self) -> bytes:
        """Returns on-chain account key."""
        return crypto.get_account_key(self.algo, self.pbk)


    def __eq__(self, other) -> bool:
        """Instance equality comparator."""
        return super().__eq__(other) and \
               self.algo == other.algo and \
               self.pbk == other.pbk


    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_PublicKey":
        return CL_PublicKey(
            crypto.KeyAlgorithm(as_bytes[0]),
            as_bytes[1:]
        )


    @staticmethod
    def from_json(as_json: str) -> "CL_PublicKey":
        return CL_PublicKey(
            crypto.KeyAlgorithm(int(as_json[0:2])),
            bytes.fromhex(as_json[2:])
        )


    def to_bytes(self) -> bytes:
        return bytes([self.algo.value]) + self.pbk


    def to_json(self) -> str:
        return self.account_key.hex()
