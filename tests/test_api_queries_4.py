# def test_get_auction_info(CLIENT):
#     def _assert(response):
#         # e.g. docs/api_reponses/rpc_state_get_auction_info.json
#         assert isinstance(response, dict)

#     _assert(CLIENT.get_auction_info())


# def test_get_era_info(CLIENT, switch_block_hash):
#     def _assert(response):
#         # e.g. docs/api_reponses/rpc_state_get_auction_info.json
#         assert isinstance(response, dict)

#     _assert(CLIENT.get_era_info(switch_block_hash))


def test_get_state_item(CLIENT, account_hash, state_root_hash):
    def _assert(response):
        assert isinstance(response, dict)

    _assert(CLIENT.get_state_item(
        f"account-hash-{account_hash.hex()}", 
        [], 
        state_root_hash)
        )
