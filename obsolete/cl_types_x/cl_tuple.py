import dataclasses
from pycspr.types.cl_types.base import CL_Type
from pycspr.types.cl_types.base import CL_TypeKey


@dataclasses.dataclass
class CL_Type_Tuple1(CL_Type):
    """Encapsulates CL type information associated with a 1-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.TUPLE_1

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.t0_type == other.t0_type


@dataclasses.dataclass
class CL_Type_Tuple2(CL_Type):
    """Encapsulates CL type information associated with a 2-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CL_Type

    # Type of first value within 2-ary tuple value.
    t1_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.TUPLE_2

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type
            

@dataclasses.dataclass
class CL_Type_Tuple3(CL_Type):
    """Encapsulates CL type information associated with a 3-ary tuple value value.

    """
    # Type of first value within 1-ary tuple value.
    t0_type: CL_Type

    # Type of first value within 2-ary tuple value.
    t1_type: CL_Type

    # Type of first value within 3-ary tuple value.
    t2_type: CL_Type

    # CSPR type key.
    type_key: CL_TypeKey = CL_TypeKey.TUPLE_3

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and \
               self.t0_type == other.t0_type and \
               self.t1_type == other.t1_type and \
               self.t2_type == other.t2_type
