from pycspr.api.node.bin import Client
from pycspr.api.node.bin.types.chain import \
    AvailableBlockRange, \
    BlockHeader, \
    ChainspecRawBytes, \
    ConsensusStatus, \
    NextUpgrade


async def test_get_information_available_block_range(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: AvailableBlockRange = \
        await NODE_BINARY_CLIENT.get_information_available_block_range(request_id=REQUEST_ID)
    assert isinstance(data, AvailableBlockRange)
    assert data.low <= data.high


async def test_get_information_block_header(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    # Block ID = None.
    data: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_block_header(REQUEST_ID, block_id=None)
    assert isinstance(data, BlockHeader)

    # Block ID = Height.
    data: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_block_header(REQUEST_ID, block_id=18)
    assert isinstance(data, BlockHeader)

    # Block ID = Hash.
    data: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_block_header(REQUEST_ID, block_id=data.parent_hash)
    assert isinstance(data, BlockHeader)


async def test_get_information_chainspec_rawbytes(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: bytes = \
        await NODE_BINARY_CLIENT.get_information_chainspec_rawbytes(request_id=REQUEST_ID)
    assert isinstance(data, ChainspecRawBytes)
    assert isinstance(data.chainspec_bytes, bytes)
    assert isinstance(data.maybe_genesis_accounts_bytes, bytes)
    assert isinstance(data.maybe_global_state_bytes, bytes)


async def test_get_information_consensus_status(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: bytes = \
        await NODE_BINARY_CLIENT.get_information_consensus_status(request_id=REQUEST_ID)
    assert isinstance(data, ConsensusStatus)


async def test_get_information_latest_switch_block_header(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data: BlockHeader = \
        await NODE_BINARY_CLIENT.get_information_latest_switch_block_header(request_id=REQUEST_ID)
    assert isinstance(data, BlockHeader)


async def test_get_information_network_name(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_network_name(request_id=REQUEST_ID)
    assert isinstance(data, str)


async def test_get_information_network_next_upgrade(NODE_BINARY_CLIENT: Client, REQUEST_ID: int):
    data = \
        await NODE_BINARY_CLIENT.get_information_network_next_upgrade(request_id=REQUEST_ID)
    assert isinstance(data, (NextUpgrade, type(None)))
