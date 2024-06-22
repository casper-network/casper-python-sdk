import typing

from pycspr.api.node.rest import serializer
from pycspr.api.node.rest.connection import ConnectionInfo
from pycspr.api.node.rest.proxy import Proxy
from pycspr.api.node.rest.types import NodeStatus
from pycspr.api.node.rest.types import ValidatorChanges


class Client():
    """Node REST server client.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self.ext = ClientExtensions(self)
        self.proxy = Proxy(connection_info)

    async def get_chainspec(self) -> dict:
        """Returns network chainspec.

        :returns: Network chainspec.

        """
        return await self.proxy.get_chainspec()

    async def get_node_metric(self, metric_id: str) -> list:
        """Returns node metrics information filtered by a particular metric.

        :param metric_id: Identifier of node metric.
        :returns: Node metrics information filtered by a particular metric.

        """
        metrics: list = await self.get_node_metrics()

        return [i for i in metrics if i.lower().startswith(metric_id.lower())]

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

        return encoded if decode is False else serializer.decode(encoded, NodeStatus)

    async def get_validator_changes(self, decode: bool = True) -> typing.List[typing.Union[dict, NodeStatus]]:
        """Returns validator change information.

        :returns: Validator change information.

        """
        encoded: dict = await self.proxy.get_validator_changes()

        return \
            encoded if decode is False else \
            [serializer.decode(i, ValidatorChanges) for i in encoded]


class ClientExtensions():
    """Node REST server client extensions, i.e. 2nd order functions.

    """
    def __init__(self, client: Client):
        """Instance constructor.

        :param client: Node RPC client.

        """
        self._client = client


    async def get_block_height(self) -> int:
        """Returns height of current block.

        :returns: Hieght of current block.

        """
        _, block_height = await self.get_chain_heights()

        return block_height

    async def get_chain_heights(self) -> typing.Tuple[int, int]:
        """Returns height of current era & block.

        :returns: 2-ary tuple: (era height, block height).

        """
        status: NodeStatus = await self._client.get_node_status()

        return \
            status.last_added_block_info.era_id, \
            status.last_added_block_info.height

    async def get_era_height(self) -> int:
        """Returns height of current era.

        :returns: Hieght of current era.

        """
        era_height, _ = await self.get_chain_heights()

        return era_height
