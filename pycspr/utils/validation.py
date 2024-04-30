import enum
import typing

from pycspr import crypto
from pycspr import factory
from pycspr.types.crypto import PublicKey
from pycspr.types.node import Block
from pycspr.types.node import Deploy
from pycspr.types.node import ValidatorWeight
from pycspr.types.node import Weight


class InvalidBlockExceptionType(enum.Enum):
    """Enumeration over set of invalid block exception types.
    
    """
    InvalidFinalitySignature = enum.auto()
    InvalidHash = enum.auto()
    InvalidProposer = enum.auto()
    InsufficientFinalitySignatureWeight = enum.auto()


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


def validate_block(
    block: Block,
    era_validator_weights: typing.List[ValidatorWeight] = None
    ):
    """Validates a block.

    :block: Block to be validated.
    :era_validator_weights: Weight of validators during the era in which the block was produced.

    """
    # Recomputed hash must match actual hash.
    # TODO: fix era_end binary serialisation error.
    # if block.hash != factory.create_digest_of_block(block.header):
    #     raise InvalidBlockException(InvalidBlockExceptionType.InvalidHash)
    
    # Proposer must be a signatory.
    if block.body.proposer not in [i.public_key for i in block.proofs]:
        raise InvalidBlockException(InvalidBlockExceptionType.InvalidProposer)

    # Signatures must be valid.
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

    # Signatures must have sufficient weight.
    if era_validator_weights is not None:
        validate_block_finality_signature_weight(block.signatories, era_validator_weights)


def validate_block_finality_signature_weight(
    signatories: typing.Set[PublicKey],
    weights: typing.List[ValidatorWeight]
    ):
    """Validates weight of finality signatures over a block.

    :signatories: A set of signatories over a block.
    :weights: A set of validator weights pertinent to the era in which the block was produced.

    """
    total_weight: int = sum([i.weight for i in weights])
    required_weight: int = int(total_weight / 3) + 1
    proven_weight: int = sum([i.weight for i in weights if i.validator in signatories])

    if proven_weight < required_weight:
        raise InvalidBlockException(InvalidBlockExceptionType.InsufficientFinalitySignatureWeight)


def validate_deploy(deploy: Deploy):
    """Validates a deploy.

    :deploy: Deploy to be validated.

    """
    # Recomputed body hash must match actual body hash.
    body_hash: bytes = factory.create_digest_of_deploy_body(deploy.payment, deploy.session)
    if deploy.header.body_hash != body_hash:
        raise InvalidDeployException(InvalidDeployExceptionType.InvalidBodyHash)

    # Recomputed hash must match actual hash.
    deploy_hash: bytes = factory.create_digest_of_deploy(deploy.header)
    if deploy.hash != deploy_hash:
        raise InvalidDeployException(InvalidDeployExceptionType.InvalidHash)

    # Signatures must be valid.
    for approval in deploy.approvals:
        if not crypto.is_signature_valid(
            deploy.hash,
            approval.signer.algo,
            approval.signature.sig,
            approval.signer.pbk,
        ):
            raise InvalidDeployException(InvalidDeployExceptionType.InvalidApproval)
