import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_Tuple1(CL_Value):
    # Associated value.
    value: object

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Tuple1":
        raise NotImplementedError()


    @staticmethod
    def from_json(as_json: str) -> "CL_Tuple1":
        raise NotImplementedError()


    def to_bytes(self) -> bytes:
        raise NotImplementedError()


    def to_json(self) -> str:
        raise NotImplementedError()
