import pytest

from pycspr import NodeEventChannel
from pycspr import NodeEventInfo
from pycspr import NodeEventType
from pycspr import NodeRpcClient
from pycspr import NodeSseClient


@pytest.mark.asyncio
async def test_await_n_blocks(SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 2
    current = RPC_CLIENT.get_block_height()
    future = current + offset
    await SSE_CLIENT.await_n_blocks(offset)
    assert RPC_CLIENT.get_block_height() == future


@pytest.mark.asyncio
async def test_await_n_eras(SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 1
    current = RPC_CLIENT.get_era_height()
    future = current + offset
    await SSE_CLIENT.await_n_eras(offset)
    assert RPC_CLIENT.get_era_height() == future


@pytest.mark.asyncio
async def test_await_n_events(SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 1
    current = RPC_CLIENT.get_block_height()
    future = current + offset
    await SSE_CLIENT.await_n_events(offset, NodeEventChannel.main, NodeEventType.BlockAdded)
    assert RPC_CLIENT.get_block_height() == future


@pytest.mark.asyncio
async def test_await_until_block_n(SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 2
    future = RPC_CLIENT.get_block_height() + offset
    await SSE_CLIENT.await_until_block_n(future)
    assert RPC_CLIENT.get_block_height() == future


@pytest.mark.asyncio
async def test_await_until_era_n(SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    offset = 1
    future = RPC_CLIENT.get_era_height() + offset
    await SSE_CLIENT.await_until_era_n(future)
    assert RPC_CLIENT.get_era_height() == future


@pytest.mark.asyncio
async def test_get_events(SSE_CLIENT: NodeSseClient, RPC_CLIENT: NodeRpcClient) -> None:
    def ecallback(einfo: NodeEventInfo):
        assert isinstance(einfo, NodeEventInfo)
        raise InterruptedError()

    try:
        SSE_CLIENT.get_events(ecallback, NodeEventChannel.main, NodeEventType.BlockAdded)
    except InterruptedError:
        pass
    else:
        raise ValueError("Event capture error")
