from pycspr.api.rest.proxy import Proxy


_ENDPOINT: str = "metrics"


def exec(proxy: Proxy) -> list:
    """Returns set of node metrics.

    :returns: Node metrics information.

    """
    response = proxy.get_response(_ENDPOINT)

    return sorted([i.strip() for i in response.split("\n") if not i.startswith("#")])
