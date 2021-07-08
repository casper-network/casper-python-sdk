from pycspr.types import CLTypeKey
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLValue



def create_cl_type_of_byte_array(size: int) -> CLType_ByteArray:
    """Returns CL type information for a byte array.
    
    :param int size: Size of byte array.

    """
    return CLType_ByteArray(size=size)


def create_cl_type_of_list(inner_type: CLType) -> CLType_List:
    """Returns CL type information for a list.
    
    :param CLType inner_type: Type information pertaining to each element within list.

    """
    return CLType_List(inner_type=inner_type)


def create_cl_type_of_map(key_type: CLType, value_type: CLType) -> CLType_Map:
    """Returns CL type information for a map.
    
    :param CLType key_type: Type information pertaining to each key within the map.
    :param CLType value_type: Type information pertaining to each value within the map.

    """
    return CLType_Map(
        key_type=key_type,
        value_type=value_type
    )


def create_cl_type_of_option(inner_type: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType inner_type: Type information pertaining to the optional value.

    """
    return CLType_Option(inner_type=inner_type)


def create_cl_type_of_simple(typeof: CLTypeKey) -> CLType_Simple:
    """Returns CL type information for a byte array.
    
    :param CLTypeKey typeof: Type of simple type being processed.

    """
    return CLType_Simple(typeof)


def create_cl_type_of_tuple_1(t0_type: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType t0_type: Type information pertaining to first tuple element.

    """
    return CLType_Tuple1(
        t0_type=t0_type
    )


def create_cl_type_of_tuple_2(t0_type: CLType, t1_type: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType t0_type: Type information pertaining to first tuple element.
    :param CLType t1_type: Type information pertaining to second tuple element.

    """
    return CLType_Tuple2(
        t0_type=t0_type,
        t1_type=t1_type
    )


def create_cl_type_of_tuple_3(t0_type: CLType, t1_type: CLType, t2_type: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType t0_type: Type information pertaining to first tuple element.
    :param CLType t1_type: Type information pertaining to second tuple element.
    :param CLType t2_type: Type information pertaining to third tuple element.

    """
    return CLType_Tuple3(
        t0_type=t0_type,
        t1_type=t1_type,
        t2_type=t2_type
    )


def create_cl_value(cl_type: CLType, parsed: object) -> CLValue:
    """Returns a value encoded for interpretation by a node.

    :param CLType cl_type: Type information for interpretation by a node.
    :param object parsed: Actual data to be processed by a node.

    """
    return CLValue(cl_type, parsed)
