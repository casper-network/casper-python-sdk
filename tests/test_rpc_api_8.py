from pycspr import NodeRpcClient
from pycspr.api.rpc import types as rpc_types


def test_get_block(RPC_CLIENT: NodeRpcClient):
    data: dict = RPC_CLIENT.get_block(decode=False)
    assert isinstance(data, dict)

    data: rpc_types.Block = RPC_CLIENT.get_block(decode=True)
    assert isinstance(data, rpc_types.Block)
