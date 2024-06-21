import enum

from pycspr import crypto
from pycspr import factory
from pycspr.types.node import Block
from pycspr.types.node import Deploy
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
    ) -> Block:
    """Validates a block.

    :block: A block to be validated.
    :parent_block: The block's parent.
    :switch_block_of_previous_era: The switch block of the previous consensus era.
    :returns: The block if considered valid, otherwise raises exception.

    """
    # TODO: extend input parameters -> blockID: if hash then ina  descent, if height then ascending & switch block must be available

    # BL-000: Verify block was sucessfully downloaded.
    if block is None:
        raise InvalidBlockException(InvalidBlockExceptionType.NotFound)

    # BL-001: Verify block hash of parent.
    # TODO: remove
    if parent_block is not None:
        if parent_block.hash != block.header.parent_hash:
            raise InvalidBlockException(InvalidBlockExceptionType.InvalidParent)

    # BL-002: Verify block hash.
    if block.hash != factory.create_digest_of_block(block.header):
        pass
        # raise InvalidBlockException(InvalidBlockExceptionType.InvalidHash)

    # Rule 4: Verify proposer is a signatory.
    # TODO: remove not absolutely necessary
    if block.body.proposer not in block.signatories:
        raise InvalidBlockException(InvalidBlockExceptionType.InvalidProposer)

    # Rule 5: Verify block signatories are era signatories.
    if switch_block_of_previous_era is not None:
        for signatory in block.signatories:
            if signatory not in switch_block_of_previous_era.header.era_end.next_era_signatories:
                raise InvalidBlockException(InvalidBlockExceptionType.InvalidProposer)

    # Rule 6: Verify finality signature authenticity.
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

    # Rule 6: Verify finality signature finality weight.
    if switch_block_of_previous_era is not None:
        validate_block_finality_signature_weight(block, switch_block_of_previous_era)

    return block


def validate_block_at_era_end(
    block: Block,
    parent_block: Block = None,
    switch_block_of_previous_era: Block = None,
    ) -> Block:
    """Validates last block in an era of consensus.

    :block: A block to be validated.
    :parent_block: The block's parent.
    :switch_block_of_previous_era: The switch block of the previous consensus era.
    :returns: The block if considered valid, otherwise raises exception.

    """
    # Rule 1: Verify block was downloaded.
    if block is None:
        raise InvalidBlockException(InvalidBlockExceptionType.NotFound)

    # Rule 2: Verify block is a switch block.
    if block.is_switch is False:
        raise InvalidBlockException(InvalidBlockExceptionType.ExpectedSwitchBlock)

    # Rule 3: Apply standard block validation rules.
    return validate_block(block, parent_block, switch_block_of_previous_era)


def validate_block_finality_signature_weight(
    block: Block,
    switch_block_of_previous_era: Block = None,
):
    proven_weight: int = \
        block.get_finality_signature_weight(switch_block_of_previous_era)
    required_weight: int = \
        switch_block_of_previous_era.validator_weight_required_for_finality_in_next_era
    if proven_weight < required_weight:
        raise InvalidBlockException(InvalidBlockExceptionType.InsufficientFinalitySignatureWeight)


def validate_deploy(deploy: Deploy) -> Deploy:
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
