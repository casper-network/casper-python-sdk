from pycspr.types.node.sse.complex import NodeEventInfo
from pycspr.types.node.sse.complex import TYPESET as _TYPESET_COMPLEX
from pycspr.types.node.sse.simple import NodeEventChannel
from pycspr.types.node.sse.simple import NodeEventType
from pycspr.types.node.sse.simple import SSE_CHANNEL_TO_SSE_EVENT
from pycspr.types.node.sse.simple import TYPESET as _TYPESET_SIMPLE

TYPESET: set = _TYPESET_COMPLEX | _TYPESET_SIMPLE
