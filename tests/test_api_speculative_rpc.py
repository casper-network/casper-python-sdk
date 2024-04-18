from pycspr import NodeSpeculativeRpcClient
from pycspr.types.node import Deploy


def test_pre_requisites(SPECULATIVE_RPC_CLIENT: NodeSpeculativeRpcClient, a_deploy: Deploy):
    assert SPECULATIVE_RPC_CLIENT is not None
    assert isinstance(a_deploy, Deploy)


async def test_deploy(SPECULATIVE_RPC_CLIENT: NodeSpeculativeRpcClient, a_deploy: Deploy):
    data: dict = await SPECULATIVE_RPC_CLIENT.speculative_exec(a_deploy)
    assert isinstance(data, dict)
    assert "Success" in data
