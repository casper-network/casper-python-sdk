from pycspr.types.node import rpc
from pycspr.types.node import sse
from pycspr.types.node.rpc import TYPESET as _TYPESET_RPC
from pycspr.types.node.sse import TYPESET as _TYPESET_SSE

TYPESET: set = _TYPESET_RPC | _TYPESET_SSE
