from pycspr import NodeRpcClient


def test_send_deploy(RPC_CLIENT: NodeRpcClient, a_deploy):
    data = RPC_CLIENT.send_deploy(a_deploy)
    assert isinstance(data, str)
    assert a_deploy.hash == bytes.fromhex(data)
