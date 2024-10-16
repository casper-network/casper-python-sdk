import typing

from pycspr.api.node.rest import Client
from pycspr.api.node.rest.type_defs import NodeStatus
from pycspr.types.node import ValidatorChanges
from pycspr.types.node import ValidatorStatusChange


async def test_that_client_is_instantiated(NODE_REST_CLIENT: Client):
    assert NODE_REST_CLIENT is not None


async def test_get_chainspec(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_chainspec()
    assert isinstance(data, dict)
    assert len(data) == 3
    assert "chainspec_bytes" in data
    assert "maybe_genesis_accounts_bytes" in data
    assert "maybe_global_state_bytes" in data


async def test_get_chain_heights_1(NODE_REST_CLIENT: Client):
    heights: typing.Tuple[int, int] = await NODE_REST_CLIENT.get_chain_heights()
    assert isinstance(heights[0], int)
    assert heights[0] > 0
    assert isinstance(heights[1], int)
    assert heights[1] > 0
    assert heights[1] > heights[0]


async def test_get_chain_heights_2(NODE_REST_CLIENT: Client):
    height: int = await NODE_REST_CLIENT.get_era_height()
    assert isinstance(height, int)
    assert height > 0


async def test_get_chain_heights_3(NODE_REST_CLIENT: Client):
    height: int = await NODE_REST_CLIENT.get_block_height()
    assert isinstance(height, int)
    assert height > 0


async def test_get_node_metrics(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_node_metrics()
    assert isinstance(data, list)
    assert len(data) > 300


async def test_get_node_metric_1(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_node_metric("address_gossiper_items_received")
    assert isinstance(data, list)
    assert len(data) == 1


async def test_get_node_metric_2(NODE_REST_CLIENT: Client):
    data = await NODE_REST_CLIENT.get_node_metric("xxxxxxxxxxxxxxxxxxxxx")
    assert isinstance(data, list)
    assert len(data) == 0


async def test_get_node_status_1(NODE_REST_CLIENT: Client):
    data: dict = await NODE_REST_CLIENT.get_node_status(decode=False)
    assert isinstance(data, dict)
    assert len(data) == 15


async def test_get_node_status_2(NODE_REST_CLIENT: Client):
    data: NodeStatus = await NODE_REST_CLIENT.get_node_status()
    assert isinstance(data, NodeStatus)


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
