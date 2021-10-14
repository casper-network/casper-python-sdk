def test_get_most_recent_block(CLIENT):
    _assert_block(CLIENT.get_block())
        

def test_get_block_by_height(CLIENT):
    for block_id in (1, 2, 3):
        _assert_block(CLIENT.get_block(block_id))


def test_get_block_by_hash(CLIENT, block_hash):
    _assert_block(CLIENT.get_block(block_hash))


def test_get_block_at_era_switch(CLIENT):
    def _assert(response):
        # e.g. docs/api_reponses/rpc_chain_get_block.json
        assert response["header"]["era_end"] is not None

    _assert(CLIENT.get_block_at_era_switch())


def test_get_block_transfers(CLIENT):
    (block_hash, transfers) = CLIENT.get_block_transfers()
    assert isinstance(block_hash, str)
    assert len(block_hash) == 64
    assert isinstance(transfers, list)
    for deploy_hash in transfers:
        assert isinstance(deploy_hash, str)
        assert len(deploy_hash) == 64


def test_get_block_transfers(CLIENT):
    (block_hash, transfers) = CLIENT.get_block_transfers()
    assert isinstance(block_hash, str)
    assert len(block_hash) == 64
    assert isinstance(transfers, list)
    for deploy_hash in transfers:
        assert isinstance(deploy_hash, bytes)
        assert len(deploy_hash) == 64


def _assert_block(block: dict):
    assert isinstance(block, dict)
    assert "body" in block        
    assert "hash" in block        
    assert "header" in block        
    assert "proofs" in block       
