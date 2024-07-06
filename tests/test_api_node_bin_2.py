from pycspr.api.node.bin import Client


async def test_get_information_block_header_endpoint(NODE_BINARY_CLIENT: Client):
    ddd = await NODE_BINARY_CLIENT.get_block_header()

    raise ValueError(ddd)
