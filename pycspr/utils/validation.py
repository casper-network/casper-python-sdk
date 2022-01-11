from pycspr import crypto
from pycspr import factory
from pycspr.types import Deploy


class InvalidDeployException():
    """Exception thrown when a deploy is deemed invalid.
    
    """
    def __init__(self, msg):
        self.msg = f"{msg}.  Deploy tampering may have occurred - review your security processes."


def validate_deploy(deploy: Deploy):
    """Validates passed deploy, raises exception when invalid.

    :deploy: Deploy to be validated.

    """
    # Validate body hash.
    body_hash: bytes = factory.create_digest_of_deploy_body(deploy.payment, deploy.session)
    if deploy.header.body_hash != body_hash:
        raise InvalidDeployException("Invalid deploy body hash")

    # Validate deploy hash.
    deploy_hash: bytes = factory.create_digest_of_deploy(deploy.header)    
    if deploy.hash != deploy_hash:
        raise InvalidDeployException("Invalid deploy hash")

    # Validate signatures.
    for approval in deploy.approvals:
        if not crypto.is_signature_valid(
            deploy.hash,
            approval.sig,
            approval.signer.pbk,
            approval.signer.algo
        ):
            raise InvalidDeployException("Invalid deploy approval signature")
