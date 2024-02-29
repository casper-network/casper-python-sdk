def test_send_deploy(CLIENT, a_deploy):
    data = CLIENT.send_deploy(a_deploy)
    assert isinstance(data, str)
    assert a_deploy.hash == bytes.fromhex(data)
