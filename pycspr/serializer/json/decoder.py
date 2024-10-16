from pycspr.serializer.json import decoder_clt
from pycspr.serializer.json import decoder_clv
from pycspr.serializer.json import decoder_crypto
from pycspr.serializer.json import decoder_node
from pycspr.types import TYPESET_CLT
from pycspr.types import TYPESET_CLV
from pycspr.types import TYPESET_NODE


def decode(typedef: object, encoded: dict) -> object:
    """Decodes a domain entity instance from JSON encoded data.

    :param typedef: Domain type to be instantiated.
    :param encoded: JSON encoded data.
    :returns: A domain type instance.

    """
    if typedef in TYPESET_CLT:
        return decoder_clt.decode(encoded)
    elif typedef in TYPESET_CLV:
        return decoder_clv.decode(encoded)
    elif typedef in TYPESET_NODE:
        return decoder_node.decode(typedef, encoded)
    else:
        raise ValueError(f"Unsupported type: {typedef}")
