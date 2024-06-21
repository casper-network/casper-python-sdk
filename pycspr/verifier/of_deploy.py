import enum

from pycspr import crypto
from pycspr import factory
from pycspr.types.node import Deploy


class InvalidDeployExceptionType(enum.Enum):
    """Enumeration over set of invalid deploy exception types.

    """
    InvalidApproval = enum.auto()
    InvalidBodyHash = enum.auto()
    InvalidHash = enum.auto()


class InvalidDeployException(Exception):
    """Exception thrown when a deploy is deemed invalid.

    """
    def __init__(self, err_type: InvalidDeployExceptionType):
        msg: str = f"Invalid deploy -> {err_type.name}"
        super(InvalidDeployException, self).__init__(msg)


def verify_deploy(deploy: Deploy) -> Deploy:
    """Validates a deploy.

    :deploy: Deploy to be validated.
    :returns: The deploy if considered valid, otherwise raises exception.

    """
    # Rule 1: Verify deploy body hash.
    body_hash: bytes = factory.create_digest_of_deploy_body(deploy.payment, deploy.session)
    if deploy.header.body_hash != body_hash:
        raise InvalidDeployException(InvalidDeployExceptionType.InvalidBodyHash)

    # Rule 2: Verify deploy hash.
    deploy_hash: bytes = factory.create_digest_of_deploy(deploy.header)
    if deploy.hash != deploy_hash:
        raise InvalidDeployException(InvalidDeployExceptionType.InvalidHash)

    # Rule 3: Verify signature authenticity.
    for approval in deploy.approvals:
        if not crypto.is_signature_valid(
            deploy.hash,
            approval.signer.algo,
            approval.signature.sig,
            approval.signer.pbk,
        ):
            raise InvalidDeployException(InvalidDeployExceptionType.InvalidApproval)

    return deploy
