import typing

from pycspr.api.node.rest.client import Client as RestClient
from pycspr.api.node.rest.connection import ConnectionInfo as RestClientConnectionInfo
from pycspr.api.node.sse.connection import ConnectionInfo
from pycspr.api.node.sse.proxy import Proxy
from pycspr.api.node.sse.types import EventInfo
from pycspr.api.node.sse.types import EventType


class Client():
    """Node SSE server client.

    """
    def __init__(self, connection_info: ConnectionInfo, rest_client: RestClient = None):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's SSE port.
        :param rest_client: Node REST client.

        """
        self.proxy = Proxy(connection_info)
        self._rest_client = rest_client or RestClient(
                RestClientConnectionInfo(
                    connection_info.host,
                    connection_info.port_rest
                )
            )

    async def await_n_blocks(self, offset: int):
        """Awaits until linear block chain has advanced by N blocks.

        :param offset: Number of blocks to await.

        """
        await self.await_n_events(
            offset,
            EventType.BlockAdded
        )

    async def await_n_eras(self, offset: int):
        """Awaits until consensus has advanced by N eras.

        :param offset: Number of eras to await.

        """
        await self.await_n_events(offset, EventType.Step)
        await self.await_n_blocks(1)

    async def await_n_events(
        self,
        offset: int,
        etype: EventType = None
    ) -> dict:
        """Awaits until the Nth event of a certain type.

        :param offset: Number of events to await.
        :param etype: Type of event type to listen for (all if unspecified).
        :returns: Event payload N events into the future.

        """
        assert offset > 0
        count = 0
        for einfo in self.yield_events(etype):
            count += 1
            if count == offset:
                return einfo.payload

    async def await_until_block_n(self, future: int) -> dict:
        """Awaits until linear block chain has advanced to block N.

        :param future: Height of a future block to await.
        :returns: On-chain block information N block in the future.

        """
        current = await self._rest_client.get_block_height()
        offset = future - current
        if offset > 0:
            await self.await_n_blocks(offset)

    async def await_until_era_n(self, future: int) -> dict:
        """Awaits until consensus has advanced to era N.

        :param future: Height of a future era to await.
        :returns: On-chain era information N eras in the future.

        """
        current = await self._rest_client.get_era_height()
        offset = future - current
        if offset > 0:
            await self.await_n_eras(offset)

    def get_events(
        self,
        etype: EventType,
        eid: int,
        ecallback: typing.Callable[[EventInfo], None]
    ):
        """Binds to a node's event stream - events are passed to callback for processing.

        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.
        :param ecallback: Callback to invoke whenever an event of relevant type is received.

        """
        for einfo in self.yield_events(etype, eid):
            ecallback(einfo)

    def yield_events(
        self,
        etype: EventType = None,
        eid: int = 0
    ) -> typing.Generator[EventInfo, None, None]:
        """Binds to a node's event stream - and yields consumed events.

        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        for einfo in self.proxy.yield_events(etype, eid):
            yield einfo
