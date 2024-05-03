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
    ExpectedSwitchBlock = enum.auto()
    NotFound = enum.auto()
    InvalidFinalitySignature = enum.auto()
    InvalidHash = enum.auto()
    InvalidParent = enum.auto()
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
    parent_block: Block = None,
    switch_block_of_previous_era: Block = None,
    ):
    """Validates a block.

    :block: A block to be validated.
    :parent_block: The block's parent.
    :switch_block_of_previous_era: The switch block of the previous consensus era.

    """
    # Rule 1: Verify block was downloaded.
    if block is None:
        raise InvalidBlockException(InvalidBlockExceptionType.NotFound)
    
    # Rule 2: Verify block's parent.
    if parent_block is not None:
        if parent_block.hash != block.header.parent_hash:
            raise InvalidBlockException(InvalidBlockExceptionType.InvalidParent)

    # Rule 3: Verify block's hash.
    if block.hash != factory.create_digest_of_block(block.header):
        pass
        # raise InvalidBlockException(InvalidBlockExceptionType.InvalidHash)
    
    # Rule 4: Verify proposer is a signatory.
    if block.body.proposer not in block.signatories:
        raise InvalidBlockException(InvalidBlockExceptionType.InvalidProposer)

    # Rule 5: Verify signature authenticity.
    block_digest_for_finality_signature: bytes = \
        factory.create_digest_of_block_for_finality_signature(block)
    for proof in block.proofs:
        if not crypto.is_signature_valid(
            block_digest_for_finality_signature,
            proof.signature.algo,
            proof.signature.sig,
            proof.public_key.pbk,
        ):
            raise InvalidBlockException(InvalidBlockExceptionType.InvalidFinalitySignature)

    # Rule 6: Verify signature finality weight.
    if switch_block_of_previous_era is not None:
        proven_weight: int = \
            block.get_finality_signature_weight(switch_block_of_previous_era)
        required_weight: int = \
            switch_block_of_previous_era.validator_weight_required_for_finality_in_next_era
        if proven_weight < required_weight:
            raise InvalidBlockException(InvalidBlockExceptionType.InsufficientFinalitySignatureWeight)

    return block


def validate_block_at_era_end(
    block: Block,
    era_validator_weights: typing.List[ValidatorWeight] = None
    ):
    """Validates last block in an era of consensus.

    :block: Switch block to be validated.
    :era_validator_weights: Weight of validators during the era in which the block was produced.

    """
    if block is None:
        raise InvalidBlockException(InvalidBlockExceptionType.NotFound)

    if block.is_switch is False:
        raise InvalidBlockException(InvalidBlockExceptionType.ExpectedSwitchBlock)

    return validate_block(block, era_validator_weights)


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
