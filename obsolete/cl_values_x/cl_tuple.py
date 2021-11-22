import dataclasses

from pycspr.types.cl_values.base import CL_Value


@dataclasses.dataclass
class CL_Tuple1(CL_Value):
    """Represents a CL type value: a 1-ary tuple.
    
    """
    # 1st value within 1-ary tuple value.
    v0: CL_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0


@dataclasses.dataclass
class CL_Tuple2(CL_Value):
    """Represents a CL type value: a 2-ary tuple.
    
    """
    # 1st value within 2-ary tuple value.
    v0: CL_Value

    # 2nd value within 2-ary tuple value.
    v1: CL_Value

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1


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

    def __eq__(self, other) -> bool:
        return self.v0 == other.v0 and self.v1 == other.v1 and self.v2 == other.v2
