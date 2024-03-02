from pycspr import NodeSpeculativeRpcClient
from pycspr.types import Deploy


def test_pre_requisites(SPECULATIVE_RPC_CLIENT: NodeSpeculativeRpcClient, a_deploy: Deploy):
    assert SPECULATIVE_RPC_CLIENT is not None
    assert isinstance(a_deploy, Deploy)


def test_deploy(SPECULATIVE_RPC_CLIENT: NodeSpeculativeRpcClient, a_deploy: Deploy):
    data: dict = SPECULATIVE_RPC_CLIENT.speculative_exec(a_deploy)
    assert isinstance(data, dict)
    assert "Success" in data
