import typing

import pycspr.serialisation.byte_array.encoder.cl_value as cl_value_encoder
import pycspr.serialisation.byte_array.encoder.deploy as deploy_encoder
from pycspr.types import CLValue


def encode(entity: object) -> bytes:
    """Encodes a domain entity as an array of bytes.

    """
    if type(entity) == CLValue:
        return cl_value_encoder.encode(entity)
    else:
        return deploy_encoder.encode(entity)
