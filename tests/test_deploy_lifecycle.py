import random



def test_that_a_new_deploy_is_unapproved(FACTORY, deploy_params, cp2):
    deploy = _create_deploy(FACTORY, deploy_params, cp2)
    assert len(deploy.approvals) == 0


def test_that_a_deploy_can_be_approved(FACTORY, deploy_params, cp1, cp2):
    deploy = _create_deploy(FACTORY, deploy_params, cp2)
    FACTORY.create_deploy_approval(cp1, deploy)
    assert len(deploy.approvals) == 1





def _create_deploy(FACTORY, deploy_params, cp2):
    return FACTORY.create_standard_transfer(
        deploy_params,
        amount = random.randint(0, 1e9),
        correlation_id = random.randint(0, 1e9),
        target = cp2.account_hash,
        )
