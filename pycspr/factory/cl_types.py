from pycspr.types.cl import CLTypeKey
from pycspr.types.cl import CLType
from pycspr.types.cl import CLType_ByteArray
from pycspr.types.cl import CLType_List
from pycspr.types.cl import CLType_Map
from pycspr.types.cl import CLType_Option
from pycspr.types.cl import CLType_Simple
from pycspr.types.cl import CLType_Tuple1
from pycspr.types.cl import CLType_Tuple2
from pycspr.types.cl import CLType_Tuple3
from pycspr.types.cl import CLValue



def create_byte_array(size: int) -> CLType_ByteArray:
    """Returns CL type information for a byte array.
    
    :param int size: Size of byte array.

    """
    return CLType_ByteArray(size=size)


def create_list(inner_type_info: CLType) -> CLType_List:
    """Returns CL type information for a list.
    
    :param CLType inner_type_info: Type information pertaining to each element within list.

    """
    return CLType_List(inner_type_info=inner_type_info)


def create_map(key_type_info: CLType, value_type_info: CLType) -> CLType_Map:
    """Returns CL type information for a map.
    
    :param CLType key_type_info: Type information pertaining to each key within the map.
    :param CLType value_type_info: Type information pertaining to each value within the map.

    """
    return CLType_Map(
        key_type_info=key_type_info,
        value_type_info=value_type_info
    )


def create_option(inner_type_info: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType inner_type_info: Type information pertaining to the optional value.

    """
    return CLType_Option(inner_type_info=inner_type_info)


def create_simple(typeof: CLTypeKey) -> CLType_Simple:
    """Returns CL type information for a byte array.
    
    :param CLTypeKey typeof: Type of simple type being processed.

    """
    return CLType_Simple(typeof)


def create_tuple_1(t0_type_info: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType t0_type_info: Type information pertaining to first tuple element.

    """
    return CLType_Tuple1(
        t0_type_info=t0_type_info
    )


def create_tuple_2(t0_type_info: CLType, t1_type_info: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType t0_type_info: Type information pertaining to first tuple element.
    :param CLType t1_type_info: Type information pertaining to second tuple element.

    """
    return CLType_Tuple2(
        t0_type_info=t0_type_info,
        t1_type_info=t1_type_info
    )


def create_tuple_3(t0_type_info: CLType, t1_type_info: CLType, t2_type_info: CLType):
    """Returns CL type information for a byte array.
    
    :param CLType t0_type_info: Type information pertaining to first tuple element.
    :param CLType t1_type_info: Type information pertaining to second tuple element.
    :param CLType t2_type_info: Type information pertaining to third tuple element.

    """
    return CLType_Tuple3(
        t0_type_info=t0_type_info,
        t1_type_info=t1_type_info,
        t2_type_info=t2_type_info
    )


def create_value(cl_type: CLTypeKey, parsed: object) -> CLValue:
    """Returns a value encoded for interpretation by a node.

    :param CLType cl_type: Type information for interpretation by a node.
    :param object parsed: Actual data to be processed by a node.

    """
    return CLValue(
        cl_type = cl_type,
        parsed = parsed
    )
