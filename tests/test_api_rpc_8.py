from pycspr import NodeRpcClient
from pycspr.types.node.rpc import Block


async def test_get_block_1(RPC_CLIENT: NodeRpcClient):
    data: dict = await RPC_CLIENT.get_block(decode=False)
    assert isinstance(data, dict)


async def test_get_block_2(RPC_CLIENT: NodeRpcClient):
    data: Block = await RPC_CLIENT.get_block(decode=True)
    assert isinstance(data, Block)
