from pycspr import NodeRpcClient
from pycspr.types.node import Block


async def test_get_block_1(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data: dict = await SIDECAR_RPC_CLIENT.get_block(decode=False)
    assert isinstance(data, dict)


async def test_get_block_2(SIDECAR_RPC_CLIENT: NodeRpcClient):
    data: Block = await SIDECAR_RPC_CLIENT.get_block(decode=True)
    assert isinstance(data, Block)
