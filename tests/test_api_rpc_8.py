from pycspr import NodeRpcClient
from pycspr.types.node.rpc import Block


async def test_get_block(RPC_CLIENT: NodeRpcClient):
    data: dict = await RPC_CLIENT.get_block(decode=False)
    assert isinstance(data, dict)

    data: Block = await RPC_CLIENT.get_block(decode=True)
    assert isinstance(data, Block)
