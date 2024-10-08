from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import \
    AvailableBlockRange, \
    BlockHeader, \
    ChainspecRawBytes, \
    ConsensusStatus, \
    NextUpgrade
from pycspr.api.node.bin.types.transport import Response


async def test_get_information_available_block_range(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: Response = \
        await NODE_BINARY_CLIENT.get_information_available_block_range(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, AvailableBlockRange)
    assert data.payload.low <= data.payload.high


async def test_get_information_block_header(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    # Block ID = None.
    data: Response = \
        await NODE_BINARY_CLIENT.get_information_block_header(REQUEST_ID, block_id=None)
    assert isinstance(data, Response)
    assert isinstance(data.payload, BlockHeader)

    # Block ID = Height.
    data: Response = \
        await NODE_BINARY_CLIENT.get_information_block_header(REQUEST_ID, block_id=18)
    assert isinstance(data, Response)
    assert isinstance(data.payload, BlockHeader)

    # Block ID = Hash.
    data: Response = \
        await NODE_BINARY_CLIENT.get_information_block_header(REQUEST_ID, block_id=data.payload.parent_hash)
    assert isinstance(data, Response)
    assert isinstance(data.payload, BlockHeader)


async def test_get_information_chainspec_rawbytes(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: bytes = \
        await NODE_BINARY_CLIENT.get_information_chainspec_rawbytes(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, ChainspecRawBytes)
    assert isinstance(data.payload.chainspec_bytes, bytes)
    assert isinstance(data.payload.maybe_genesis_accounts_bytes, bytes)
    assert isinstance(data.payload.maybe_global_state_bytes, bytes)


async def test_get_information_consensus_status(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: bytes = \
        await NODE_BINARY_CLIENT.get_information_consensus_status(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, ConsensusStatus)


async def test_get_information_latest_switch_block_header(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_latest_switch_block_header(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, BlockHeader)


async def test_get_information_network_name(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_network_name(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, str)


async def test_get_information_network_next_upgrade(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_network_next_upgrade(request_id=REQUEST_ID)
    assert isinstance(data, Response)
    assert isinstance(data.payload, (NextUpgrade, type(None)))
