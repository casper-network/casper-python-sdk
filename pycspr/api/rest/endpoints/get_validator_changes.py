import json

from pycspr.api.rest.proxy import Proxy


_ENDPOINT: str = "validator-changes"


def exec(proxy: Proxy) -> list:
    """Returns validator change information.

    :returns: Validator change information.

    """
    return json.loads(proxy.get_response(_ENDPOINT))
