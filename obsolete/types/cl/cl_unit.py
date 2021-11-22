import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_Unit(CL_Value):
    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Unit":
        if len(as_bytes) != 0:
            raise ValueError("Invalid unit bytes")
        return CL_Unit()


    @staticmethod
    def from_json(as_json: str) -> "CL_Unit":
        if len(as_json) != 0:
            raise ValueError("Invalid unit json")
        return CL_Unit()


    def to_bytes(self) -> bytes:
        return bytes([])


    def to_json(self) -> str:
        return ""
