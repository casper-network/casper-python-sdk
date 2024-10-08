import typing

from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import BlockSynchronizerStatus
from pycspr.api.node.bin.types.node import NodePeerEntry, NodeUptime
from pycspr.api.node.bin.types.primitives.time import Timestamp
from pycspr.api.node.bin.types.transport import Response


async def test_get_information_node_block_synchronizer_status(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    # TODO: explore how to ensure node is in fast sync mode.
    data = \
        await NODE_BINARY_CLIENT.get_information_node_block_synchronizer_status(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, (BlockSynchronizerStatus, type(None)))


async def test_get_information_node_last_progress(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_node_last_progress(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, Timestamp)


async def test_get_information_node_peers(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: typing.List[NodePeerEntry] = \
        await NODE_BINARY_CLIENT.get_information_node_peers(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, list)
    for entity in data.payload:
        assert isinstance(entity, NodePeerEntry)
        assert isinstance(entity.address, str)
        assert isinstance(entity.node_id, str)


async def test_get_information_node_reactor_state(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_node_reactor_state(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, str)


async def test_get_information_node_uptime(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: NodeUptime = \
        await NODE_BINARY_CLIENT.get_information_node_uptime(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, int)
