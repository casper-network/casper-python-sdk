from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rest import endpoints
from pycspr.api.rest.proxy import Proxy


class Client():
    """Node REST server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection: Information required to connect to a node.

        """
        self.ext = ClientExtensions(self)
        self.proxy = Proxy(connection_info.host, connection_info.port_rest)

    def get_chainspec(self) -> list:
        """Returns network chainspec.

        :returns: Network chainspec.

        """
        return endpoints.get_chainspec(self.proxy)


    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return endpoints.get_metrics(self.proxy)

    def get_node_status(self) -> list:
        """Returns node status information.

        :returns: Node status information.

        """
        return endpoints.get_status(self.proxy)

    def get_node_rpc_schema(self) -> list:
        """Returns node RPC API schema.

        :returns: Node RPC API schema.

        """
        return endpoints.get_rpc_schema(self.proxy)

    def get_validator_changes(self) -> list:
        """Returns validator change information.

        :returns: Validator change information.

        """
        return endpoints.get_validator_changes(self.proxy)


class ClientExtensions():
    """Node REST server client extensions, i.e. 2nd order functions.

    """
    def __init__(self, client: Client):
        """Instance constructor.

        :param client: Node REST client.

        """
        self.client = client

    def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        metrics: list = self.client.get_node_metrics()

        return [i for i in metrics if i.lower().startswith(metric_id.lower())]
