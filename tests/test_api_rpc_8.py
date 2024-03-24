from pycspr import NodeRpcClient
from pycspr.types.api.rpc import Block


def test_get_block(RPC_CLIENT: NodeRpcClient):
    data: dict = RPC_CLIENT.get_block(decode=False)
    assert isinstance(data, dict)

    data: Block = RPC_CLIENT.get_block(decode=True)
    assert isinstance(data, Block)
