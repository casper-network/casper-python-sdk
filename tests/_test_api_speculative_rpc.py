from pycspr import NodeSpeculativeRpcClient
from pycspr.types.node import Deploy


def test_pre_requisites(SIDECAR_SPECULATIVE_RPC_CLIENT: NodeSpeculativeRpcClient, a_deploy: Deploy):
    assert SIDECAR_SPECULATIVE_RPC_CLIENT is not None
    assert isinstance(a_deploy, Deploy)


async def test_deploy(SIDECAR_SPECULATIVE_RPC_CLIENT: NodeSpeculativeRpcClient, a_deploy: Deploy):
    data: dict = await SIDECAR_SPECULATIVE_RPC_CLIENT.speculative_exec(a_deploy)
    assert isinstance(data, dict)
    assert "Success" in data
