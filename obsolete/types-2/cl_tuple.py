import dataclasses

from pycspr.types.cl_value import CL_Value


@dataclasses.dataclass
class CL_Tuple1(CL_Value):
    """Represents a CL type value: a 1-ary tuple.
    
    """
    # 1st value within 1-ary tuple value.
    v0: CL_Value

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0

    def as_bytes(self) -> bytes:
        raise NotImplementedError()

    def as_cl_type(self) -> "CL_Tuple1":
        raise NotImplementedError()

    def as_parsed(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Tuple1":
        raise NotImplementedError()

    #endregion


@dataclasses.dataclass
class CL_Tuple2(CL_Value):
    """Represents a CL type value: a 2-ary tuple.
    
    """
    # 1st value within 2-ary tuple value.
    v0: CL_Value

    # 2nd value within 2-ary tuple value.
    v1: CL_Value

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1

    def as_bytes(self) -> bytes:
        raise NotImplementedError()

    def as_cl_type(self) -> "CL_Tuple2":
        raise NotImplementedError()

    def as_parsed(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Tuple2":
        raise NotImplementedError()

    #endregion


@dataclasses.dataclass
class CL_Tuple3(CL_Value):
    """Represents a CL type value: a 3-ary tuple.
    
    """
    # 1st value within 3-ary tuple value.
    v0: CL_Value

    # 2nd value within 3-ary tuple value.
    v1: CL_Value

    # 3rd value within 3-ary tuple value.
    v2: CL_Value

    #region Equality & serialisation

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1 and self.v2 == other.v2

    def as_bytes(self) -> bytes:
        raise NotImplementedError()

    def as_cl_type(self) -> "CL_Tuple3":
        raise NotImplementedError()

    def as_parsed(self) -> str:
        raise NotImplementedError()

    @staticmethod
    def from_bytes(as_bytes: bytes) -> "CL_Tuple3":
        raise NotImplementedError()

    #endregion
