def test_can_send_a_deploy(LIB, a_test_deploy):
    def _assert(response):
        assert isinstance(response, str)
        assert a_test_deploy.hash == bytes.fromhex(response)

    _assert(LIB.send_deploy(a_test_deploy))
