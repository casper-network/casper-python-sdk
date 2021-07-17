def test_can_send_a_deploy(CLIENT, a_deploy):
    def _assert(response):
        assert isinstance(response, str)
        assert a_deploy.hash == bytes.fromhex(response)

    _assert(CLIENT.deploys.send(a_deploy))
