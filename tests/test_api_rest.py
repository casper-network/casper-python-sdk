from pycspr.api.node.rest import Client
from pycspr.api.node.rest.types import NodeStatus

from pycspr.types.node import ValidatorChanges, ValidatorStatusChange


async def test_get_chainspec(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_chainspec()
    assert isinstance(data, dict)
    assert len(data) == 3
    assert "chainspec_bytes" in data
    assert "maybe_genesis_accounts_bytes" in data
    assert "maybe_global_state_bytes" in data


async def test_get_node_metrics(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_node_metrics()
    assert isinstance(data, list)
    assert len(data) > 300


async def test_get_node_metric(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_node_metric("mem_deploy_gossiper")
    assert isinstance(data, list)
    assert len(data) == 1

    data = await NODE_REST_CLIENT.get_node_metric("xxxxxxxxxxxxxxxxxxxxx")
    assert isinstance(data, list)
    assert len(data) == 0


async def test_get_node_status_1(NODE_REST_CLIENT: Client):
    data: dict = await NODE_REST_CLIENT.get_node_status(decode=False)
    assert isinstance(data, dict)
    assert len(data) == 14


async def test_get_node_status_2(NODE_REST_CLIENT: Client):
    data: NodeStatus = await NODE_REST_CLIENT.get_node_status()
    print(NodeStatus)
    print(type(data))
    assert isinstance(data, NodeStatus)


async def test_get_node_rpc_schema(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_node_rpc_schema()
    assert isinstance(data, dict)
    assert len(data) == 5


async def test_get_validator_changes_1(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_validator_changes(decode=False)
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)


async def test_get_validator_changes_2(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_validator_changes()
    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, ValidatorChanges)
