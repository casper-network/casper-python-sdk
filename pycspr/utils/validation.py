import enum

from pycspr import crypto
from pycspr import factory
from pycspr.types.node import Block
from pycspr.types.node import Deploy


class InvalidBlockExceptionType(enum.Enum):
    """Enumeration over set of invalid block exception types.
    
    """
    InvalidFinalitySignature = enum.auto()
    InvalidHash = enum.auto()
    InvalidProposer = enum.auto()


class InvalidBlockException(Exception):
    """Exception thrown when a block is deemed invalid.

    """
    def __init__(self, err_type: InvalidBlockExceptionType):
        msg: str = f"Invalid block -> {err_type.name}"
        super(InvalidBlockException, self).__init__(msg)


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


def validate_block(block: Block):
    """Validates a block, raises exception when invalid.

    :block: Block to be validated.

    """
    # Validate that computed block hash matches.
    if block.hash != factory.create_digest_of_block(block.header):
        raise InvalidBlockException(InvalidBlockExceptionType.InvalidHash)
    
    # Validate that block proposer signed over block.
    if block.body.proposer not in [i.public_key for i in block.proofs]:
        raise InvalidBlockException(InvalidBlockExceptionType.InvalidProposer)

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
            raise InvalidBlockException(InvalidBlockExceptionType.InvalidFinalitySignature)

    raise InvalidBlockException(InvalidBlockExceptionType.InvalidProposer)


def validate_deploy(deploy: Deploy):
    """Validates a deploy, raises exception when invalid.

    :deploy: Deploy to be validated.

    """
    body_hash: bytes = factory.create_digest_of_deploy_body(deploy.payment, deploy.session)
    if deploy.header.body_hash != body_hash:
        raise InvalidDeployException(InvalidDeployExceptionType.InvalidBodyHash)

    deploy_hash: bytes = factory.create_digest_of_deploy(deploy.header)
    if deploy.hash != deploy_hash:
        raise InvalidDeployException(InvalidDeployExceptionType.InvalidHash)

    for approval in deploy.approvals:
        if not crypto.is_signature_valid(
            deploy.hash,
            approval.signer.algo,
            approval.signature.sig,
            approval.signer.pbk,
        ):
            raise InvalidDeployException(InvalidDeployExceptionType.InvalidApproval)
