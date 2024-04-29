from pycspr import crypto
from pycspr import factory
from pycspr.types.node import Block
from pycspr.types.node import Deploy


class InvalidBlockException(Exception):
    """Exception thrown when a block is deemed invalid.

    """
    def __init__(self, msg):
        self.msg = f"{msg}. block tampering may have occurred - review security process."


class InvalidDeployException(Exception):
    """Exception thrown when a deploy is deemed invalid.

    """
    def __init__(self, msg):
        self.msg = f"{msg}. Deploy tampering may have occurred - review security process."


def validate_block(block: Block):
    """Validates a block, raises exception when invalid.

    :block: Block to be validated.

    """
    # Validate that computed block hash matches.
    if block.hash != factory.create_digest_of_block(block.header):
        raise InvalidBlockException("Invalid block hash")
    
    # Validate that block proposer signed over block.
    if block.body.proposer not in [i.public_key for i in block.proofs]:
        raise InvalidBlockException("Invalid proposer")

    # Validate that finality signature proofs are valid.
    digest_of_block_for_finality_signature: bytes = \
        factory.create_digest_of_block_for_finality_signature(block)
    for proof in block.proofs:
        if not crypto.is_signature_valid(
            digest_of_block_for_finality_signature,
            proof.signature.algo,
            proof.signature.sig,
            proof.public_key.pbk,
        ):
            raise InvalidBlockException("Invalid block signature")


def validate_deploy(deploy: Deploy):
    """Validates a deploy, raises exception when invalid.

    :deploy: Deploy to be validated.

    """
    body_hash: bytes = factory.create_digest_of_deploy_body(deploy.payment, deploy.session)
    if deploy.header.body_hash != body_hash:
        raise InvalidDeployException("Invalid deploy body hash")

    deploy_hash: bytes = factory.create_digest_of_deploy(deploy.header)
    if deploy.hash != deploy_hash:
        raise InvalidDeployException("Invalid deploy hash")

    for approval in deploy.approvals:
        print(
            deploy.hash.hex(),
            approval.signer.algo,
            approval.signature.sig.hex(),
            approval.signer.pbk.hex()
            )
        if not crypto.is_signature_valid(
            deploy.hash,
            approval.signer.algo,
            approval.signature.sig,
            approval.signer.pbk,
        ):
            raise InvalidDeployException("Invalid deploy approval signature")
