import json

from pycspr.api.rest.utils.proxy import Proxy


_ENDPOINT: str = "chainspec"


def exec(proxy: Proxy) -> list:
    """Returns network chainspec.

    :returns: Network chainspec.

    """
    return json.loads(proxy.get_response(_ENDPOINT))
