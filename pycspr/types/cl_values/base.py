import abc
import dataclasses
import typing
from pycspr.types.cl_types import CL_Type


@dataclasses.dataclass
class CL_Value():
    """Represents a CL type value.
    
    """
    @abc.abstractmethod
    def as_bytes(self) -> bytes:
        pass

    @abc.abstractmethod
    def as_cl_type(self) -> CL_Type:
        pass

    @abc.abstractmethod
    def as_parsed(self) -> str:
        pass    

    def as_json(self) -> dict:
        return {
            "cl_type": self.as_cl_type().as_json(),
            "bytes": self.as_bytes(),
            "parsed": self.as_parsed()
        }

    def from_json(self, obj: dict) -> "CL_Value":
        print(obj)
