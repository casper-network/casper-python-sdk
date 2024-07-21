from pycspr.api.node.bin import Client


# async def test_get_block_header_endpoint(NODE_BINARY_CLIENT: Client):
#     ddd = await NODE_BINARY_CLIENT.get_information_block_header(request_id=256)

#     raise ValueError(ddd)


async def test_get_uptime_endpoint_1(NODE_BINARY_CLIENT: Client):
    ddd = await NODE_BINARY_CLIENT.get_information_uptime_1()

    raise ValueError(ddd)


# async def test_get_uptime_endpoint(NODE_BINARY_CLIENT: Client):
#     ddd = await NODE_BINARY_CLIENT.get_information_uptime()

#     raise ValueError(ddd)
