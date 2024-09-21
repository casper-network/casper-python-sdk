from pycspr import NodeRpcClient
from pycspr.types.node import Deploy


async def test_send_deploy(SIDECAR_RPC_CLIENT: NodeRpcClient, a_deploy: Deploy):
    data = await SIDECAR_RPC_CLIENT.send_deploy(a_deploy)
    assert isinstance(data, str)
    assert a_deploy.hash == bytes.fromhex(data)
