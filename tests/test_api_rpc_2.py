from pycspr import NodeRpcClient
from pycspr.types.api.rpc import ValidatorChanges


def test_get_node_peers(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_node_peers()

    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)


def test_get_node_status(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_node_status()

    assert isinstance(data, dict)


def test_get_validator_changes(RPC_CLIENT: NodeRpcClient):
    data = RPC_CLIENT.get_validator_changes()

    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, ValidatorChanges)
