import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey


@dataclasses.dataclass
class CL_Type_Any(CL_Type):
    """Encapsulates CL type information associated with any value.

    """
    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.ANY

    def as_bytes(self) -> bytes:
        return bytes([self.type_key.value])

    def as_json(self) -> str:
        return "Any"

    @staticmethod
    def from_bytes(_: bytes) -> "CL_Type_Any":
        return CL_Type_Any()

    @staticmethod
    def from_json(_: str) -> "CL_Type_Any":
        return CL_Type_Any()
