import random

import pytest

from pycspr import NodeBinaryClient
from pycspr.api.node.bin.types.chain import BlockHeader


@pytest.fixture(scope="session")
async def BLOCK_HEADER(NODE_BINARY_CLIENT: NodeBinaryClient) -> BlockHeader:
    """Returns most recent block.

    """
    request_id = random.randint(0, int(1e2))
    response = await NODE_BINARY_CLIENT.information.get_block_header(request_id)

    return response.payload
