from pycspr.api.node.bin import Client


async def test_that_client_is_instantiated(NODE_BINARY_CLIENT: Client):
    assert NODE_BINARY_CLIENT is not None
