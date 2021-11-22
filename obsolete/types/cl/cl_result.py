import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_Result(CL_Value):
    # Associated value.
    value: object

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Result":
        raise NotImplementedError()


    @staticmethod
    def from_json(as_json: str) -> "CL_Result":
        raise NotImplementedError()


    def to_bytes(self) -> bytes:
        raise NotImplementedError()


    def to_json(self) -> str:
        raise NotImplementedError()
