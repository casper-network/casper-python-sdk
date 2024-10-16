from pycspr.types import node
from pycspr.types import cl

from pycspr.types.cl import TYPESET as TYPESET_CL
from pycspr.types.cl import TYPESET_CLT
from pycspr.types.cl import TYPESET_CLV
from pycspr.types.node import TYPESET as TYPESET_NODE

TYPESET: set = TYPESET_CL | TYPESET_NODE
