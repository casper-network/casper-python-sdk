import pycspr


def test_get_node_peers_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):    
    data = RPC_CLIENT.get_node_peers()

    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)


def test_get_node_status_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    data = RPC_CLIENT.get_node_status()

    assert isinstance(data, dict)


def test_get_validator_changes_with_rpc_client(RPC_CLIENT: pycspr.NodeRpcClient):
    data = RPC_CLIENT.get_validator_changes()

    assert isinstance(data, list)
    for item in data:
        assert isinstance(item, dict)
