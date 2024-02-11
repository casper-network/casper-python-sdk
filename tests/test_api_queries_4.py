def test_get_most_recent_block(CLIENT):
    _assert_block(CLIENT.get_block())


def test_get_block_by_height(CLIENT):
    for block_id in (1, 2, 3):
        _assert_block(CLIENT.get_block(block_id))


def test_get_block_by_hash(CLIENT, block_hash):
    _assert_block(CLIENT.get_block(block_hash))


def test_get_block_at_era_switch(CLIENT):
    def _assert(response):
        assert isinstance(response, dict)

    _assert(CLIENT.get_block_at_era_switch())


def test_get_era_info(CLIENT, switch_block_hash):
    def _assert(response):
        assert isinstance(response, dict)

    _assert(CLIENT.get_era_info(switch_block_hash))


def test_get_era_summary(CLIENT, block_hash):
    def _assert(response):
        assert isinstance(response, dict)

    _assert(CLIENT.get_era_summary(block_hash))


def test_get_state_item(CLIENT, account_hash, state_root_hash):
    def _assert(response):
        assert isinstance(response, dict)

    _assert(CLIENT.get_state_item(
        f"account-hash-{account_hash.hex()}",
        [],
        state_root_hash)
        )
