import dataclasses

from pycspr.types.cl.cl_value import CL_Value


@dataclasses.dataclass
class CL_Bool(CL_Value):
    # Associated value.
    value: bool

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Bool":
        return CL_Bool(bool(as_bytes[0]))


    @staticmethod
    def from_json(as_json: str) -> "CL_Bool":
        if as_json == "False":
            return CL_Bool(False)
        elif as_json == "True":
            return CL_Bool(True)
        else:
            raise ValueError("Invalid boolean JSON string representation")


    def to_bytes(self) -> bytes:
        return bytes([int(self.value)])


    def to_json(self) -> str:
        return str(self.value)
