import typing

from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import AvailableBlockRange, BlockHeader
from pycspr.api.node.bin.types.node import NodePeerEntry, NodeUptime


async def test_get_information_available_block_range(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: AvailableBlockRange = \
        await NODE_BINARY_CLIENT.get_information_available_block_range(request_id=REQUEST_ID)
    assert isinstance(data, AvailableBlockRange)
    assert data.low <= data.high


async def test_get_information_block_header(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data_1: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_block_header(block_id=18, request_id=REQUEST_ID)
    assert isinstance(data_1, BlockHeader)

    data_2: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_block_header(block_id=data_1.parent_hash, request_id=REQUEST_ID)
    assert isinstance(data_2, BlockHeader)


async def test_get_information_node_peers(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: typing.List[NodePeerEntry] = \
        await NODE_BINARY_CLIENT.get_information_node_peers(request_id=REQUEST_ID)
    assert isinstance(data, list)
    for entity in data:
        assert isinstance(entity, NodePeerEntry)
        assert isinstance(entity.address, str)
        assert isinstance(entity.node_id, str)


async def test_get_information_node_reactor_state(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_node_reactor_state(request_id=REQUEST_ID)
    assert isinstance(data, str)


async def test_get_information_node_uptime(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: NodeUptime = \
        await NODE_BINARY_CLIENT.get_information_node_uptime(request_id=REQUEST_ID)
    assert isinstance(data, int)
