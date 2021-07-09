import random



def test_deploy_is_unapproved_when_instantiated(FACTORY, deploy_params, cp2):
    deploy = _create_deploy(FACTORY, deploy_params, cp2)
    assert len(deploy.approvals) == 0


def test_deploy_can_be_approved(FACTORY, deploy_params, cp1, cp2):
    deploy = _create_deploy(FACTORY, deploy_params, cp2)
    deploy.set_approval(cp1)
    assert len(deploy.approvals) == 1
    assert deploy.approvals[0].signer == cp1.account_key


def test_deploy_can_be_approved_by_multiple_parties(FACTORY, deploy_params, cp1, cp2):
    deploy = _create_deploy(FACTORY, deploy_params, cp2)
    deploy.set_approval(cp1)
    deploy.set_approval(cp2)
    assert len(deploy.approvals) == 2


def test_deploy_approvals_are_deduplicated(FACTORY, deploy_params, cp1, cp2):
    deploy = _create_deploy(FACTORY, deploy_params, cp2)
    for _ in range(10):
        deploy.set_approval(cp1)
        deploy.set_approval(cp2)
    assert len(deploy.approvals) == 2


def _create_deploy(FACTORY, deploy_params, cp2):
    return FACTORY.create_standard_transfer(
        deploy_params,
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = cp2.account_hash,
        )
