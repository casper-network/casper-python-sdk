from pycspr.api.node.bin.types.requests import get_information as information
from pycspr.api.node.bin.types.requests import get_record as record
from pycspr.api.node.bin.types.requests import get_state as state

PAYLOAD_TYPESET = information.PAYLOAD_TYPESET | record.PAYLOAD_TYPESET | state.PAYLOAD_TYPESET
