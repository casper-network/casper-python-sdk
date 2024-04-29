import os
import pathlib
import tempfile

import pycspr


def test_that_deploy_is_unapproved_when_instantiated(deploy_params, cp2):
    deploy = _create_deploy(deploy_params, cp2)
    assert len(deploy.approvals) == 0


def test_that_deploy_can_be_approved(deploy_params, cp1, cp2):
    deploy = _create_deploy(deploy_params, cp2)
    deploy.set_approval(pycspr.factory.create_deploy_approval(deploy, cp1))
    assert len(deploy.approvals) == 1
    assert deploy.approvals[0].signer == cp1.to_public_key()


def test_that_deploy_can_be_approved_by_multiple_parties(deploy_params, cp1, cp2):
    deploy = _create_deploy(deploy_params, cp2)
    deploy.set_approval(pycspr.factory.create_deploy_approval(deploy, cp1))
    deploy.set_approval(pycspr.factory.create_deploy_approval(deploy, cp2))
    assert len(deploy.approvals) == 2


def test_that_deploy_approvals_are_deduplicated(deploy_params, cp1, cp2):
    deploy = _create_deploy(deploy_params, cp2)
    for _ in range(10):
        deploy.set_approval(pycspr.factory.create_deploy_approval(deploy, cp1))
        deploy.set_approval(pycspr.factory.create_deploy_approval(deploy, cp2))
    assert len(deploy.approvals) == 2


def test_that_a_deploy_can_be_written_to_fs(deploy_params, cp1, cp2):
    deploy = _create_deploy(deploy_params, cp2)
    with tempfile.TemporaryFile() as fp:
        fpath = str(fp)
        pycspr.write_deploy(deploy, fpath)
        assert os.path.exists(fpath)
        os.remove(fpath)


def test_that_a_deploy_can_be_written_to_and_read_from_fs(deploy_params, cp1, cp2):
    deploy_1 = _create_deploy(deploy_params, cp2)
    with tempfile.TemporaryFile() as fp:
        fpath = str(fp)
        pycspr.write_deploy(deploy_1, fpath)
        deploy_2 = pycspr.read_deploy(fpath)
        assert isinstance(deploy_2, type(deploy_1))
        assert pycspr.serializer.to_json(deploy_1) == \
               pycspr.serializer.to_json(deploy_2)
        os.remove(fpath)


def _create_deploy(deploy_params, cp2):
    return pycspr.factory.create_transfer(
        deploy_params,
        amount=123456789,
        target=cp2.to_public_key(),
        correlation_id=1
        )
