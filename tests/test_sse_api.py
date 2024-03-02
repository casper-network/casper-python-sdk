import pytest

from pycspr import NodeRpcClient
from pycspr import NodeSseClient
from pycspr import SSE_CHANNEL_TO_SSE_EVENT


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
