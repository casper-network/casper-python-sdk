from pycspr import NodeRpcClient
from pycspr.types import Deploy


def test_send_deploy(RPC_CLIENT: NodeRpcClient, a_deploy: Deploy):
    data = RPC_CLIENT.send_deploy(a_deploy)
    assert isinstance(data, str)
    assert a_deploy.hash == bytes.fromhex(data)
