import typing

from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import BlockHeader
from pycspr.api.node.bin.types.node import NodePeerEntry, NodeUptime


async def test_get_information_block_header(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_block_header(block_id=18, request_id=REQUEST_ID)

    assert isinstance(data, BlockHeader)


# async def test_get_information_node_peers(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
#     data: typing.List[NodePeerEntry] = \
#         await NODE_BINARY_CLIENT.get_information_node_peers(request_id=REQUEST_ID)

#     assert isinstance(data, list)
#     for entity in data:
#         assert isinstance(entity, NodePeerEntry)
#         assert isinstance(entity.address, str)
#         assert isinstance(entity.node_id, str)


# async def test_get_information_node_uptime(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
#     data: NodeUptime = \
#         await NODE_BINARY_CLIENT.get_information_node_uptime(request_id=REQUEST_ID)

#     assert isinstance(data, int)
