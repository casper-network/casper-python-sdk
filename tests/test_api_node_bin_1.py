from pycspr.api.node.bin import Client


async def test_that_client_is_instantiated(NODE_BINARY_CLIENT: Client):
    assert NODE_BINARY_CLIENT is not None


async def test_that_client_is_instantiated_and_request_id_is_generated(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    assert NODE_BINARY_CLIENT is not None
    assert REQUEST_ID > 0
