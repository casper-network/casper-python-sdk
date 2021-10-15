from pycspr.types import CLType
from pycspr.types import CLValue


def create_cl_value(cl_type: CLType, parsed: object) -> CLValue:
    """Returns a value encoded for interpretation by a node.

    :param CLType cl_type: Type information for interpretation by a node.
    :param object parsed: Actual data to be processed by a node.

    """
    return CLValue(cl_type, parsed)
