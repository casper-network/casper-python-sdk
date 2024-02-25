import typing

from pycspr.api.connection import NodeConnectionInfo
from pycspr.api.rpc import Client as RpcClient
from pycspr.api.sse.proxy import Proxy
from pycspr.api.sse.types import NodeEventChannel
from pycspr.api.sse.types import NodeEventInfo
from pycspr.api.sse.types import NodeEventType
from pycspr.api.sse.types import SSE_CHANNEL_TO_SSE_EVENT


class Client():
    """Node SSE server client.

    """
    def __init__(self, connection_info: NodeConnectionInfo, rpc_client: RpcClient = None):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.
        :param rpc_client: Node RPC client.

        """
        self.ext = ClientExtensions(self, rpc_client or RpcClient(connection_info))
        self.proxy = Proxy(connection_info.host, connection_info.port_sse)

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
    def __init__(self, client: Client, rpc_client: RpcClient):
        """Instance constructor.

        :param client: Node SSE client.
        :param rpc_client: Node RPC client.

        """
        self.client = client
        self.rpc_client = rpc_client

    async def await_n_blocks(self, offset: int):
        """Awaits until linear block chain has advanced by N blocks.

        :param offset: Number of blocks to await.

        """
        await self.await_n_events(NodeEventChannel.main, NodeEventType.BlockAdded, offset)

    async def await_n_eras(self, offset: int):
        """Awaits until consensus has advanced by N eras.

        :param offset: Number of eras to await.

        """
        await self.await_n_events(NodeEventChannel.main, NodeEventType.Step, offset)
        await self.await_n_blocks(1)

    async def await_n_events(
        self,
        echannel: NodeEventChannel,
        etype: NodeEventType,
        offset: int
    ) -> dict:
        """Awaits emission of N events of a certain type over a certain channel.

        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :param offset: Number of events to await.
        :returns: Event payload N events into the future.

        """
        assert offset > 0
        count = 0
        for einfo in self.client.yield_events(echannel, etype):
            count += 1
            if count == offset:
                return einfo.payload

    async def await_until_block_n(self, block_height: int) -> dict:
        """Awaits until linear block chain has advanced to block N.

        :param block_height: Hieght of block to await.
        :returns: On-chain block information at block N blocks.

        """
        _, block_height_current = self.rpc_client.ext.get_chain_heights()
        offset = block_height - block_height_current
        if offset > 0:
            await self.await_n_blocks(offset)

    async def await_until_era_n(self, era_height: int) -> dict:
        """Awaits until consensus has advanced to era N.

        :param era_height: Height of era to await.
        :returns: On-chain era information N eras in the future.

        """
        era_height_current, _ = self.rpc_client.ext.get_chain_heights()
        offset = era_height - era_height_current
        if offset > 0:
            await self.await_n_eras(offset)

    def get_events(
        self,
        on_event_callback: typing.Callable[[NodeEventInfo], None],
        echannel: NodeEventChannel,
        etype: NodeEventType = None,
        eid: int = 0
    ):
        """Binds to a node's event stream - events are passed to callback for processing.

        :param on_event_callback: Callback to invoke whenever an event of relevant type is received.
        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        for einfo in self.client.yield_events(echannel, etype, eid):
            on_event_callback(einfo)
