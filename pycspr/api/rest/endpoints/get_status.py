import json

from pycspr.api.rest.proxy import Proxy


_ENDPOINT: str = "status"


def exec(proxy: Proxy) -> list:
    """Returns set of node metrics.

    :returns: Node metrics information.

    """
    return json.loads(proxy.get_response(_ENDPOINT))
