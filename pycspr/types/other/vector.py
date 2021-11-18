import dataclasses
import typing

from pycspr.types.cl_values.base import CL_Value
from pycspr.types.cl_values.cl_int import CL_U32


@dataclasses.dataclass
class Vector(CL_Value):
    # Associated vector.
    vec: typing.List[bytes]

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "Vector":
        raise NotImplementedError()


    @staticmethod
    def from_json(as_json: str) -> "Vector":
        raise NotImplementedError()


    def to_bytes(self) -> bytes:
        return CL_U32(len(self.vec)).to_bytes() + \
               bytes([i for j in self.vec for i in j])


    def to_json(self) -> str:
        raise NotImplementedError()
