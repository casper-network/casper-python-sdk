from pycspr.api.node.bin import Client


# async def test_get_information_chainspec_raw_bytes(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
#     ddd = await NODE_BINARY_CLIENT.get_information_chainspec_raw_bytes(request_id=REQUEST_ID)

#     raise ValueError(ddd)


async def test_get_information_uptime(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    ddd = await NODE_BINARY_CLIENT.get_information_uptime(request_id=REQUEST_ID)

    raise ValueError(ddd)
