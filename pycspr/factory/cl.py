from pycspr.types import CLStorageKeyType
from pycspr.types import CLTypeKey
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_StorageKey
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLValue



def create_cl_value(cl_type: CLType, parsed: object) -> CLValue:
    """Returns a value encoded for interpretation by a node.

    :param CLType cl_type: Type information for interpretation by a node.
    :param object parsed: Actual data to be processed by a node.

    """
    return CLValue(cl_type, parsed)
