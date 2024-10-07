import typing

from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.node import NodePeerEntry, NodeUptime


async def test_get_information_node_last_progress(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_node_last_progress(request_id=REQUEST_ID)
    assert isinstance(data, int)


# async def test_get_information_node_peers(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
#     data: typing.List[NodePeerEntry] = \
#         await NODE_BINARY_CLIENT.get_information_node_peers(request_id=REQUEST_ID)
#     assert isinstance(data, list)
#     for entity in data:
#         assert isinstance(entity, NodePeerEntry)
#         assert isinstance(entity.address, str)
#         assert isinstance(entity.node_id, str)


# async def test_get_information_node_reactor_state(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
#     data = \
#         await NODE_BINARY_CLIENT.get_information_node_reactor_state(request_id=REQUEST_ID)
#     assert isinstance(data, str)


# async def test_get_information_node_uptime(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
#     data: NodeUptime = \
#         await NODE_BINARY_CLIENT.get_information_node_uptime(request_id=REQUEST_ID)
#     assert isinstance(data, int)
