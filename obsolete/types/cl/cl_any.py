import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_Any(CL_Value):
    # Associated value.
    value: object

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Any":
        raise NotImplementedError()


    @staticmethod
    def from_json(as_json: str) -> "CL_Any":
        raise NotImplementedError()


    def to_bytes(self) -> bytes:
        raise NotImplementedError()


    def to_json(self) -> str:
        raise NotImplementedError()
