import dataclasses
import typing

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_Option(CL_Value):
    # Associated value.
    value: typing.Union[None, CL_Value]


    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Option":
        raise NotImplementedError()


    @staticmethod
    def from_json(as_json: str) -> "CL_Option":
        raise NotImplementedError()


    def to_bytes(self) -> bytes:
        if self.value:
            return bytes([1]) + self.value.to_bytes()
        else:
            return bytes([0])


    def to_json(self) -> str:
        raise NotImplementedError()
