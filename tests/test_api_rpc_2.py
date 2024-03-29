import typing

from pycspr import NodeRpcClient
from pycspr.types.node.rpc import ValidatorChanges
from pycspr.types.node.rpc import NodePeer
from pycspr.types.node.rpc import NodeStatus


async def test_get_node_peers(RPC_CLIENT: NodeRpcClient):
    data: typing.List[dict] = await RPC_CLIENT.get_node_peers(decode=False)
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)

    data: typing.List[NodePeer]  = await RPC_CLIENT.get_node_peers(decode=True)
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, NodePeer)


async def test_get_node_status(RPC_CLIENT: NodeRpcClient):
    data: dict = await RPC_CLIENT.get_node_status(decode=False)
    assert isinstance(data, dict)

    data: NodeStatus = await RPC_CLIENT.get_node_status(decode=True)
    assert isinstance(data, NodeStatus)
    assert isinstance(data.peers, list)
    for item in data.peers:
        assert isinstance(item, NodePeer)


async def test_get_validator_changes(RPC_CLIENT: NodeRpcClient):
    data = await RPC_CLIENT.get_validator_changes()

    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, ValidatorChanges)
