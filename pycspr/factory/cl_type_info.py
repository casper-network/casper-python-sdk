from pycspr.types.cl import CLType
from pycspr.types.cl import CLTypeInfo
from pycspr.types.cl import CLTypeInfoForByteArray
from pycspr.types.cl import CLTypeInfoForList
from pycspr.types.cl import CLTypeInfoForMap
from pycspr.types.cl import CLTypeInfoForOption
from pycspr.types.cl import CLTypeInfoForSimple
from pycspr.types.cl import CLTypeInfoForTuple1
from pycspr.types.cl import CLTypeInfoForTuple2
from pycspr.types.cl import CLTypeInfoForTuple3



def create_byte_array(size: int) -> CLTypeInfoForByteArray:
    """Returns CL type information for a byte array.
    
    :param int size: Size of byte array.

    """
    return CLTypeInfoForByteArray(
        typeof=CLType.BYTE_ARRAY,
        size=size
    )


def create_list(inner_type_info: CLTypeInfo) -> CLTypeInfoForList:
    """Returns CL type information for a list.
    
    :param CLTypeInfo inner_type_info: Type information pertaining to each element within list.

    """
    return CLTypeInfoForList(
        typeof=CLType.LIST,
        inner_type_info=inner_type_info
    )


def create_map(key_type_info: CLTypeInfo, value_type_info: CLTypeInfo) -> CLTypeInfoForMap:
    """Returns CL type information for a map.
    
    :param CLTypeInfo key_type_info: Type information pertaining to each key within the map.
    :param CLTypeInfo value_type_info: Type information pertaining to each value within the map.

    """
    return CLTypeInfoForMap(
        typeof=CLType.MAP,
        key_type_info=key_type_info,
        value_type_info=value_type_info
    )


def create_option(inner_type_info: CLTypeInfo):
    """Returns CL type information for a byte array.
    
    :param CLTypeInfo inner_type_info: Type information pertaining to the optional value.

    """
    return CLTypeInfoForOption(
        typeof=CLType.OPTION,
        inner_type_info=inner_type_info
    )


def create_simple(typeof: CLType) -> CLTypeInfoForSimple:
    """Returns CL type information for a byte array.
    
    :param CLType typeof: Type of simple type being processed.

    """
    return CLTypeInfoForSimple(typeof)


def create_tuple_1(t0_type_info: CLTypeInfo):
    """Returns CL type information for a byte array.
    
    :param CLTypeInfo t0_type_info: Type information pertaining to first tuple element.

    """
    return CLTypeInfoForTuple1(
        typeof=CLType.TUPLE_1,
        t0_type_info=t0_type_info
    )


def create_tuple_2(t0_type_info: CLTypeInfo, t1_type_info: CLTypeInfo):
    """Returns CL type information for a byte array.
    
    :param CLTypeInfo t0_type_info: Type information pertaining to first tuple element.
    :param CLTypeInfo t1_type_info: Type information pertaining to second tuple element.

    """
    return CLTypeInfoForTuple2(
        typeof=CLType.TUPLE_1,
        t0_type_info=t0_type_info,
        t1_type_info=t1_type_info
    )


def create_tuple_3(t0_type_info: CLTypeInfo, t1_type_info: CLTypeInfo, t2_type_info: CLTypeInfo):
    """Returns CL type information for a byte array.
    
    :param CLTypeInfo t0_type_info: Type information pertaining to first tuple element.
    :param CLTypeInfo t1_type_info: Type information pertaining to second tuple element.
    :param CLTypeInfo t2_type_info: Type information pertaining to third tuple element.

    """
    return CLTypeInfoForTuple3(
        typeof=CLType.TUPLE_1,
        t0_type_info=t0_type_info,
        t1_type_info=t1_type_info,
        t2_type_info=t2_type_info
    )
