import typing

from pycspr.api.rest.connection import ConnectionInfo
from pycspr.api.rest.proxy import Proxy
from pycspr.serializer.json.node_rpc import decoder as rpc_decoder
from pycspr.types.node.rpc import NodeStatus
from pycspr.types.node.rpc import ValidatorChanges


class Client():
    """Node REST server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.proxy = Proxy(connection_info)

        # Extension methods -> 2nd order functions.
        ext = ClientExtensions(self)
        self.get_node_metric = ext.get_node_metric

    async def get_chainspec(self) -> dict:
        """Returns network chainspec.

        :returns: Network chainspec.

        """
        return await self.proxy.get_chainspec()

    async def get_node_metrics(self) -> list:
        """Returns set of node metrics.

        :returns: Node metrics information.

        """
        return await self.proxy.get_node_metrics()

    async def get_node_status(self, decode: bool = True) -> typing.Union[dict, NodeStatus]:
        """Returns node status information.

        :param decode: Flag indicating whether to decode API response.
        :returns: Node status information.

        """
        encoded: dict = await self.proxy.get_node_status()

        return encoded if decode is False else rpc_decoder.decode(encoded, NodeStatus)

    async def get_node_rpc_schema(self) -> dict:
        """Returns node RPC API schema.

        :returns: Node RPC API schema.

        """
        return await self.proxy.get_rpc_schema()

    async def get_validator_changes(self, decode: bool = True) -> list:
        """Returns validator change information.

        :returns: Validator change information.

        """
        encoded: dict = await self.proxy.get_validator_changes()

        return \
            encoded if decode is False else \
            [rpc_decoder.decode(i, ValidatorChanges) for i in encoded]


class ClientExtensions():
    """Node REST server client extensions, i.e. 2nd order functions.

    """
    def __init__(self, client: Client):
        """Instance constructor.

        :param client: Node REST client.

        """
        self.client = client

    async def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        metrics: list = await self.client.get_node_metrics()

        return [i for i in metrics if i.lower().startswith(metric_id.lower())]
