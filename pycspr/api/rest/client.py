from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rest.proxy import Proxy


class Client():
    """Node REST server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo):
        """Instance constructor.

        :param connection: Information required to connect to a node.

        """
        self.proxy = Proxy(connection_info.host, connection_info.port_rest)

        # Extension methods -> 2nd order functions.
        ext = ClientExtensions(self)
        self.get_node_metric = ext.get_node_metric

    def get_chainspec(self) -> dict:
        """Returns network chainspec.

        :returns: Network chainspec.

        """
        return self.proxy.get_chainspec()

    def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return self.proxy.get_node_metrics()

    def get_node_status(self) -> dict:
        """Returns node status information.

        :returns: Node status information.

        """
        return self.proxy.get_node_status()

    def get_node_rpc_schema(self) -> dict:
        """Returns node RPC API schema.

        :returns: Node RPC API schema.

        """
        return self.proxy.get_rpc_schema()

    def get_validator_changes(self) -> list:
        """Returns validator change information.

        :returns: Validator change information.

        """
        return self.proxy.get_validator_changes()


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
