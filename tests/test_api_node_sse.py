from pycspr.api.node.rest import Client as RestClient
from pycspr.api.node.sse import Client
from pycspr.api.node.sse import EventInfo
from pycspr.api.node.sse import EventType


async def test_that_client_is_instantiated(NODE_SSE_CLIENT: Client):
    assert NODE_SSE_CLIENT is not None


async def test_await_n_blocks(NODE_SSE_CLIENT: Client, NODE_REST_CLIENT: RestClient) -> None:
    offset = 2
    current = await NODE_REST_CLIENT.get_block_height()
    future = current + offset
    await NODE_SSE_CLIENT.await_n_blocks(offset)
    assert await NODE_REST_CLIENT.get_block_height() == future


async def test_await_n_eras(NODE_SSE_CLIENT: Client, NODE_REST_CLIENT: RestClient) -> None:
    offset = 1
    current = await NODE_REST_CLIENT.get_era_height()
    future = current + offset
    await NODE_SSE_CLIENT.await_n_eras(offset)
    assert await NODE_REST_CLIENT.get_era_height() == future


async def test_await_n_events(NODE_SSE_CLIENT: Client, NODE_REST_CLIENT: RestClient) -> None:
    offset = 1
    current = await NODE_REST_CLIENT.get_block_height()
    future = current + offset
    await NODE_SSE_CLIENT.await_n_events(offset, EventType.BlockAdded)
    assert await NODE_REST_CLIENT.get_block_height() == future


async def test_get_events(NODE_SSE_CLIENT: Client) -> None:
    def ecallback(einfo: EventInfo):
        assert isinstance(einfo, EventInfo)
        raise InterruptedError()

    try:
        NODE_SSE_CLIENT.get_events(EventType.BlockAdded, 0, ecallback)
    except InterruptedError:
        pass
    else:
        raise ValueError("Event capture error")


async def test_yield_events(NODE_SSE_CLIENT: Client) -> None:
    events: int = 0
    for einfo in NODE_SSE_CLIENT.yield_events(EventType.BlockAdded):
        assert isinstance(einfo, EventInfo)
        events += 1
        if events == 5:
            break
