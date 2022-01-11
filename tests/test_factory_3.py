import pycspr


def test_deploy_size_in_bytes(deploy_params, cp1, cp2):
    deploy = _create_deploy(deploy_params, cp1, cp2)
    assert pycspr.get_deploy_size_bytes(deploy) == 394


def test_deploy_validation_1(deploy_params, cp1, cp2):
    deploy = _create_deploy(deploy_params, cp1, cp2)
    assert pycspr.validate_deploy(deploy) is None


def _create_deploy(deploy_params, cp1, cp2):
    deploy = pycspr.factory.create_transfer(
        deploy_params,
        amount=123456789,
        target=cp2.account_key,
        correlation_id=1
        )
    deploy.approve(cp1)

    return deploy
