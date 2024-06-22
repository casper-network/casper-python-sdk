import typing

from pycspr.api.node.rest.client import Client as RestClient
from pycspr.api.node.rest.connection import ConnectionInfo as RestClientConnectionInfo
from pycspr.api.node.sse.connection import ConnectionInfo
from pycspr.api.node.sse.proxy import Proxy
from pycspr.api.node.sse.types import NodeEventChannel
from pycspr.api.node.sse.types import NodeEventInfo
from pycspr.api.node.sse.types import NodeEventType
from pycspr.api.node.sse.types import SSE_CHANNEL_TO_SSE_EVENT


class Client():
    """Node SSE server client.

    """
    def __init__(self, connection_info: ConnectionInfo, rest_client: RestClient = None):
        """Instance constructor.

        :param connection_info: Information required to connect to a node's SSE port.
        :param rest_client: Node REST client.

        """
        self.proxy = Proxy(connection_info)
        if rest_client is None:
            rest_client = RestClient(
                RestClientConnectionInfo(
                    connection_info.host,
                    connection_info.port_rest
                )
            )
        self.ext = ClientExtensions(self, rest_client)


    def yield_events(
        self,
        echannel: NodeEventChannel,
        etype: NodeEventType = None,
        eid: int = 0
    ) -> typing.Generator[NodeEventInfo, None, None]:
        """Binds to a node's event stream - and yields consumed events.

        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        if echannel not in SSE_CHANNEL_TO_SSE_EVENT:
            raise ValueError(f"Unsupported SSE channel: {echannel.name}.")
        if etype is not None and etype not in SSE_CHANNEL_TO_SSE_EVENT[echannel]:
            raise ValueError(f"Unsupported channel/event: {echannel.name}:{etype.name}.")

        for einfo in self.proxy.yield_events(echannel, etype, eid):
            yield einfo


class ClientExtensions():
    """Node SSE server client extensions, i.e. 2nd order functions.

    """
    def __init__(self, client: Client):
        """Instance constructor.

        :param client: Node SSE client.

        """
        self.client = client
        self.rest_client = client.rpc

    async def await_n_blocks(self, offset: int):
        """Awaits until linear block chain has advanced by N blocks.

        :param offset: Number of blocks to await.

        """
        await self.await_n_events(offset, NodeEventChannel.main, NodeEventType.BlockAdded)

    async def await_n_eras(self, offset: int):
        """Awaits until consensus has advanced by N eras.

        :param offset: Number of eras to await.

        """
        await self.await_n_events(offset, NodeEventChannel.main, NodeEventType.Step)
        await self.await_n_blocks(1)

    async def await_n_events(
        self,
        offset: int,
        echannel: NodeEventChannel,
        etype: NodeEventType = None
    ) -> dict:
        """Awaits emission of N events of a certain type over a certain channel.

        :param offset: Number of events to await.
        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :returns: Event payload N events into the future.

        """
        assert offset > 0
        count = 0
        for einfo in self.client.yield_events(echannel, etype):
            count += 1
            if count == offset:
                return einfo.payload

    async def await_until_block_n(self, future: int) -> dict:
        """Awaits until linear block chain has advanced to block N.

        :param future: Height of a future block to await.
        :returns: On-chain block information N block in the future.

        """
        current = await self.rest_client.ext.get_block_height()
        offset = future - current
        if offset > 0:
            await self.await_n_blocks(offset)

    async def await_until_era_n(self, future: int) -> dict:
        """Awaits until consensus has advanced to era N.

        :param future: Height of a future era to await.
        :returns: On-chain era information N eras in the future.

        """
        current = await self.rest_client.ext.get_era_height()
        offset = future - current
        if offset > 0:
            await self.await_n_eras(offset)

    def get_events(
        self,
        ecallback: typing.Callable[[NodeEventInfo], None],
        echannel: NodeEventChannel,
        etype: NodeEventType = None,
        eid: int = 0
    ):
        """Binds to a node's event stream - events are passed to callback for processing.

        :param ecallback: Callback to invoke whenever an event of relevant type is received.
        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        for einfo in self.client.yield_events(echannel, etype, eid):
            ecallback(einfo)
