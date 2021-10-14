import requests as rest_client

from pycspr.api import constants
from pycspr.api.connection import NodeConnection



def execute(node: NodeConnection, metric_id: str = None) -> list:
    """Returns node peers information.

    :param node: Information required to connect to a node.
    :param metric_id: Identifier of node metric.

    :returns: Node metrics information.

    """
    endpoint = f"{node.address_rest}/{constants.REST_GET_METRICS}"
    response = rest_client.get(endpoint)
    data = response.content.decode("utf-8")
    metrics = sorted([i.strip() for i in data.split("\n") if not i.startswith("#")])

    return metrics if metric_id is None else \
           [i for i in metrics if i.lower().startswith(metric_id.lower())]
