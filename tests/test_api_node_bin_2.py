import typing

from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.node import NodePeerEntry
from pycspr.api.node.bin.types.node import NodeUptime


async def test_get_information_node_peers(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: typing.List[NodePeerEntry] = \
        await NODE_BINARY_CLIENT.get_information_node_peers(request_id=REQUEST_ID)

    assert isinstance(data, list)
    for entity in data:
        assert isinstance(entity, NodePeerEntry)
        assert isinstance(entity.address, str)
        assert isinstance(entity.node_id, str)


async def test_get_information_node_uptime(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: NodeUptime = \
        await NODE_BINARY_CLIENT.get_information_node_uptime(request_id=REQUEST_ID)

    assert isinstance(data, int)
