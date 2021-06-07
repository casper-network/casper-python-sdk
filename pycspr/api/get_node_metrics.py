import requests as rest_client

import pycspr



# API endpoint to be invoked.
_API_ENDPOINT = "metrics"


def execute(
    metric_id: str = None,
    ) -> list:
    """Returns node peers information.

    :param metric_id: Identifier of node metric.

    :returns: Node metrics information.

    """
    endpoint = f"{pycspr.CONNECTION.address_rest}/{_API_ENDPOINT}"
    response = rest_client.get(endpoint).content.decode("utf-8")
    response = sorted([i.strip() for i in response.split("\n") if not i.startswith("#")])

    return response if metric_id is None else \
           [i for i in response if i.lower().startswith(metric_id.lower())]
