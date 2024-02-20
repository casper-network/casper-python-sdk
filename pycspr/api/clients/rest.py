from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.servers import rest as SERVER


class RestServerClient():
    """Node REST server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection: Information required to connect to a node.

        """
        self.proxy = SERVER.Proxy(
            host=connection_info.host,
            port=connection_info.port_rest
        )

    def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        return [i for i in self.get_node_metrics() if i.lower().startswith(metric_id.lower())]

    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return SERVER.get_metrics(self.proxy)
