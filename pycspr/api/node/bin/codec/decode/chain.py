import typing

from pycspr.api.node.bin.codec.constants import \
    TAG_ACTIVATION_POINT_ERA, \
    TAG_ACTIVATION_POINT_GENESIS, \
    TAG_BLOCK_TYPE_V1, \
    TAG_BLOCK_TYPE_V2
from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.type_defs.chain import \
    ActivationPoint, \
    ActivationPoint_Era, \
    ActivationPoint_Genesis, \
    AvailableBlockRange, \
    Block, \
    Block_V1, \
    Block_V2, \
    BlockBody_V1, \
    BlockBody_V2, \
    BlockBodyHash, \
    BlockHash, \
    BlockHeader, \
    BlockHeader_V1, \
    BlockHeader_V2, \
    BlockHeight, \
    BlockSignatures, \
    BlockSignatures_V1, \
    BlockSignatures_V2, \
    BlockSynchronizerStatus, \
    BlockSynchronizerStatusInfo, \
    ChainNameDigest, \
    ChainspecRawBytes, \
    ConsensusReward, \
    ConsensusStatus, \
    ConsensusValidatorChanges, \
    DelegationRate, \
    EraEnd_V1, \
    EraEnd_V2, \
    EraID, \
    EraValidatorReward, \
    EraValidatorWeight, \
    GasPrice, \
    Motes, \
    NextUpgrade, \
    ProtocolVersion, \
    RewardedSignatures, \
    SignedBlock, \
    SingleBlockRewardedSignatures, \
    Transaction, \
    Transaction_V1, \
    Transaction_V2, \
    ValidatorID, \
    Weight
from pycspr.type_defs.crypto import DigestBytes, PublicKey, PublicKeyBytes, Signature
from pycspr.type_defs.primitives import U8, U32, U64, U512, TimeDifference, Timestamp


def _decode_activation_point(bytes_in: bytes) -> typing.Tuple[bytes, ActivationPoint]:
    rem, type_tag = decode(U8, bytes_in)
    if type_tag == TAG_ACTIVATION_POINT_ERA:
        return _decode_activation_point_era_id(rem)
    elif type_tag == TAG_ACTIVATION_POINT_GENESIS:
        return _decode_activation_point_genesis(rem)
    else:
        raise ValueError("Invalid type tag: activation point ")


def _decode_activation_point_era_id(bytes_in: bytes) -> typing.Tuple[bytes, ActivationPoint_Era]:
    rem, era_id = decode(EraID, bytes_in)

    return rem, ActivationPoint_Era(era_id)


def _decode_activation_point_genesis(bytes_in: bytes) -> typing.Tuple[bytes, ActivationPoint_Genesis]:
    rem, timestamp = decode(Timestamp, bytes_in)

    return rem, ActivationPoint_Genesis(timestamp)


def _decode_available_block_range(bytes_in: bytes) -> typing.Tuple[bytes, AvailableBlockRange]:
    rem, low = decode(U64, bytes_in)
    rem, high = decode(U64, rem)

    return rem, AvailableBlockRange(low, high)


def _decode_block(bytes_in: bytes) -> typing.Tuple[bytes, Block]:
    rem, type_tag = decode(U8, bytes_in)
    if type_tag == TAG_BLOCK_TYPE_V1:
        return decode(Block_V1, rem)
    elif type_tag == TAG_BLOCK_TYPE_V2:
        return decode(Block_V2, rem)
    else:
        raise ValueError("Invalid type tag: block ")


def _decode_block_v1(bytes_in: bytes) -> typing.Tuple[bytes, Block_V1]:
    rem, digest = decode(BlockHash, bytes_in)
    rem, header = decode(BlockHeader_V1, rem)
    rem, body = decode(BlockBody_V1, rem)

    return rem, Block_V1(body, digest, header)


def _decode_block_v2(bytes_in: bytes) -> typing.Tuple[bytes, Block_V2]:
    rem, digest = decode(BlockHash, bytes_in)
    rem, header = decode(BlockHeader_V2, rem)
    rem, body = decode(BlockBody_V2, rem)

    return rem, Block_V2(body, digest, header)


def _decode_block_body_v1(bytes_in: bytes) -> typing.Tuple[bytes, BlockBody_V1]:
    raise NotImplementedError("_decode_block_body_v1")


def _decode_block_body_v2(bytes_in: bytes) -> typing.Tuple[bytes, BlockBody_V2]:
    # TODO: Transactions -> Map: U8 <-> Tx-Hash
    transactions = dict()
    rem, size = decode(U32, bytes_in)

    rem, rewarded_signatures = decode(RewardedSignatures, rem)

    return rem, BlockBody_V2(None, rewarded_signatures, transactions)


def _decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    rem, type_tag = decode(U8, bytes_in)
    if type_tag == TAG_BLOCK_TYPE_V1:
        return _decode_block_header_v1(rem)
    elif type_tag == TAG_BLOCK_TYPE_V2:
        return _decode_block_header_v2(rem)
    else:
        raise ValueError("Invalid type tag: block header")


def _decode_block_header_v1(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V1]:
    raise NotImplementedError()


def _decode_block_header_v2(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V2]:
    rem, parent_block_hash = decode(BlockHash, bytes_in)
    rem, state_root_hash = decode(DigestBytes, rem)
    rem, body_hash = decode(BlockBodyHash, rem)
    rem, random_bit = decode(bool, rem)
    rem, accumulated_seed = decode(DigestBytes, rem)
    rem, era_end = decode(EraEnd_V2, rem, is_optional=True)
    rem, timestamp = decode(Timestamp, rem)
    rem, era_id = decode(EraID, rem)
    rem, height = decode(BlockHeight, rem)
    rem, protocol_version = decode(ProtocolVersion, rem)
    rem, proposer = decode(PublicKeyBytes, rem)
    rem, current_gas_price = decode(GasPrice, rem)
    rem, last_switch_block_hash = decode(DigestBytes, rem, is_optional=True)

    return rem, BlockHeader_V2(
        accumulated_seed=accumulated_seed,
        body_hash=body_hash,
        current_gas_price=current_gas_price,
        era_end=era_end,
        era_id=era_id,
        height=height,
        last_switch_block_hash=last_switch_block_hash,
        parent_hash=parent_block_hash,
        proposer=proposer,
        protocol_version=protocol_version,
        random_bit=random_bit,
        state_root_hash=state_root_hash,
        timestamp=timestamp
    )


def _decode_block_signatures(bytes_in: bytes) -> typing.Tuple[bytes, BlockSignatures]:
    rem, type_tag = decode(U8, bytes_in)
    if type_tag == TAG_BLOCK_TYPE_V1:
        return _decode_block_signatures_v1(rem)
    elif type_tag == TAG_BLOCK_TYPE_V2:
        return _decode_block_signatures_v2(rem)
    else:
        raise ValueError("Invalid type tag: block signatures")


def _decode_block_signatures_v1(bytes_in: bytes) -> typing.Tuple[bytes, BlockSignatures_V1]:
    raise NotImplementedError("_decode_block_signatures_v1")


def _decode_block_signatures_v2(bytes_in: bytes) -> typing.Tuple[bytes, BlockSignatures_V2]:
    rem, block_hash = decode(BlockHash, bytes_in)
    rem, block_height = decode(BlockHeight, rem)
    rem, era_id = decode(EraID, rem)
    rem, chain_name_hash = decode(ChainNameDigest, rem)
    rem, proofs = decode((PublicKey, Signature), rem)

    return rem, BlockSignatures_V2(
        block_hash=block_hash,
        block_height=block_height,
        era_id=era_id,
        chain_name_hash=chain_name_hash,
        proofs=proofs,
    )


def _decode_block_synchronizer_status(bytes_in: bytes) -> typing.Tuple[bytes, BlockSynchronizerStatus]:
    rem, historical = decode(BlockSynchronizerStatusInfo, bytes_in, is_optional=True)
    rem, forward = decode(BlockSynchronizerStatusInfo, rem, is_optional=True)

    if historical is None and forward is None:
        return rem, None
    else:
        return rem, BlockSynchronizerStatus(historical, forward)


def _decode_block_synchronizer_status_info(bytes_in: bytes) -> typing.Tuple[bytes, BlockSynchronizerStatusInfo]:
    rem, block_hash = decode(BlockHash, bytes_in)
    rem, block_height = decode(BlockHeight, rem, is_optional=True)
    rem, acquisition_state = decode(str, rem)

    return rem, BlockSynchronizerStatusInfo(block_hash, block_height, acquisition_state)


def _decode_chainspec_raw_bytes(bytes_in: bytes) -> typing.Tuple[bytes, ChainspecRawBytes]:
    rem, chainspec_bytes = decode(bytes, bytes_in)
    rem, genesis_accounts_bytes = decode(bytes, rem, is_optional=True)
    rem, global_state_bytes = decode(bytes, rem, is_optional=True)

    return rem, ChainspecRawBytes(chainspec_bytes, genesis_accounts_bytes, global_state_bytes)


def _decode_consensus_reward(bytes_in: bytes) -> typing.Tuple[bytes, ConsensusReward]:
    rem, amount = decode(Motes, bytes_in)
    rem, era_id = decode(EraID, rem)
    rem, delegation_rate = decode(DelegationRate, rem)
    rem, switch_block_hash = decode(DigestBytes, rem)

    return rem, ConsensusReward(amount, era_id, delegation_rate, switch_block_hash)


def _decode_consensus_state(bytes_in: bytes) -> typing.Tuple[bytes, ConsensusStatus]:
    rem, validator_public_key = decode(PublicKey, bytes_in)
    rem, round_length = decode(TimeDifference, rem, is_optional=True)

    return rem, ConsensusStatus(validator_public_key, round_length)


def _decode_consensus_validator_changes(bytes_in: bytes) -> typing.Tuple[bytes, ConsensusValidatorChanges]:
    rem, size = decode(U32, bytes_in)
    if size == 0:
        return rem, dict()


def _decode_era_end_v1(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V1]:
    raise NotImplementedError()


def _decode_era_end_v2(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V2]:
    rem, equivocators = decode(ValidatorID, bytes_in, is_sequence=True)
    rem, inactive_validators = decode(ValidatorID, rem, is_sequence=True)
    rem, next_era_validator_weights = decode(EraValidatorWeight, rem, is_sequence=True)
    rem, rewards = decode(EraValidatorReward, rem, is_sequence=True)
    rem, next_era_gas_price = decode(GasPrice, rem)

    return rem, EraEnd_V2(
        equivocators=equivocators,
        inactive_validators=inactive_validators,
        next_era_gas_price=next_era_gas_price,
        next_era_validator_weights=next_era_validator_weights,
        rewards=rewards
    )


def _decode_era_validator_reward(bytes_in: bytes) -> typing.Tuple[bytes, EraValidatorReward]:
    rem, validator_id = decode(ValidatorID, bytes_in)
    rem, rewards = decode(Motes, rem, is_sequence=True)

    return rem, EraValidatorReward(rewards, validator_id)


def _decode_era_validator_weight(bytes_in: bytes) -> typing.Tuple[bytes, EraValidatorWeight]:
    rem, validator_id = decode(ValidatorID, bytes_in)
    rem, weight = decode(Weight, rem)

    return rem, EraValidatorWeight(validator_id, weight)


def _decode_next_upgrade(bytes_in: bytes) -> typing.Tuple[bytes, NextUpgrade]:
    rem, activation_point = decode(ActivationPoint, bytes_in)
    rem, protocol_version = decode(ProtocolVersion, rem)

    return rem, NextUpgrade(activation_point, protocol_version)


def _decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    rem, major = decode(U32, bytes_in)
    rem, minor = decode(U32, rem)
    rem, patch = decode(U32, rem)

    return rem, ProtocolVersion(major, minor, patch)


def _decode_rewarded_signatures(bytes_in: bytes) -> typing.Tuple[bytes, RewardedSignatures]:
    f = []
    rem, size = decode(U32, bytes_in)
    for _ in range(size):
        rem, sigs = decode(SingleBlockRewardedSignatures, rem)
        f.append(sigs)

    return rem, f


def _decode_signed_block(bytes_in: bytes) -> typing.Tuple[bytes, SignedBlock]:
    rem, block = decode(Block, bytes_in)
    rem, signatures = decode(BlockSignatures, rem)

    return rem, SignedBlock(block, signatures)


def _decode_single_block_rewarded_signatures(bytes_in: bytes) -> typing.Tuple[bytes, SingleBlockRewardedSignatures]:
    return decode(bytes, bytes_in)


register_decoders({
    (BlockBodyHash, lambda x: decode(DigestBytes, x)),
    (BlockHash, lambda x: decode(DigestBytes, x)),
    (BlockHeight, lambda x: decode(U64, x)),
    (ChainNameDigest, lambda x: decode(DigestBytes, x)),
    (DelegationRate, lambda x: decode(U8, x)),
    (EraID, lambda x: decode(U64, x)),
    (GasPrice, lambda x: decode(U8, x)),
    (Motes, lambda x: decode(U512, x)),
    (Weight, lambda x: decode(U512, x)),
})

register_decoders({
    (ActivationPoint, _decode_activation_point),
    (AvailableBlockRange, _decode_available_block_range),
    (Block, _decode_block),
    (Block_V1, _decode_block_v1),
    (Block_V2, _decode_block_v2),
    (BlockBody_V1, _decode_block_body_v1),
    (BlockBody_V2, _decode_block_body_v2),
    (BlockHeader, _decode_block_header),
    (BlockHeader_V1, _decode_block_header_v1),
    (BlockHeader_V2, _decode_block_header_v2),
    (BlockSignatures, _decode_block_signatures),
    (BlockSignatures_V1, _decode_block_signatures_v1),
    (BlockSignatures_V2, _decode_block_signatures_v2),
    (BlockSynchronizerStatus, _decode_block_synchronizer_status),
    (BlockSynchronizerStatusInfo, _decode_block_synchronizer_status_info),
    (ChainspecRawBytes, _decode_chainspec_raw_bytes),
    (ConsensusReward, _decode_consensus_reward),
    (ConsensusStatus, _decode_consensus_state),
    (ConsensusValidatorChanges, _decode_consensus_validator_changes),
    (EraEnd_V1, _decode_era_end_v1),
    (EraEnd_V2, _decode_era_end_v2),
    (EraValidatorReward, _decode_era_validator_reward),
    (EraValidatorWeight, _decode_era_validator_weight),
    (NextUpgrade, _decode_next_upgrade),
    (ProtocolVersion, _decode_protocol_version),
    (RewardedSignatures, _decode_rewarded_signatures),
    (SignedBlock, _decode_signed_block),
    (SingleBlockRewardedSignatures, _decode_single_block_rewarded_signatures),
    (ValidatorID, lambda x: decode(PublicKey, x)),
})
