import dataclasses

from pycspr.types.cl_value import CL_Value


@dataclasses.dataclass
class CL_Map(CL_Value):
    # Associated value.
    value: object

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        raise NotImplementedError()

    def as_bytes(self) -> bytes:
        raise NotImplementedError()

    def as_cl_type(self) -> "CL_Map":
        raise NotImplementedError()

    def as_parsed(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Map":
        raise NotImplementedError()

    #endregion
