import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.codec.chain import constants
from pycspr.api.node.bin.types.chain.complex import \
    ActivationPoint, \
    ActivationPoint_Era, \
    ActivationPoint_Genesis, \
    AvailableBlockRange, \
    BlockHeader, \
    BlockHeader_V1, \
    BlockHeader_V2, \
    BlockSynchronizerStatus, \
    BlockSynchronizerStatusInfo, \
    ChainspecRawBytes, \
    ConsensusStatus, \
    EraEnd_V1, \
    EraEnd_V2, \
    EraValidatorReward, \
    EraValidatorWeight, \
    NextUpgrade, \
    ProtocolVersion, \
    ValidatorID
from pycspr.api.node.bin.types.chain.simple import \
    BlockBodyHash, \
    BlockHash, \
    BlockHeight, \
    EraID, \
    GasPrice, \
    Motes, \
    Weight
from pycspr.api.node.bin.types.primitives.crypto import DigestBytes, PublicKey, PublicKeyBytes
from pycspr.api.node.bin.types.primitives.numeric import U8, U32, U64
from pycspr.api.node.bin.types.primitives.time import TimeDifference, Timestamp


def _decode_activation_point(bytes_in: bytes) -> typing.Tuple[bytes, ActivationPoint]:
    bytes_rem, type_tag = decode(U8, bytes_in)
    if type_tag == constants.TAG_ACTIVATION_POINT_ERA:
        return _decode_activation_point_era_id(bytes_rem)
    elif type_tag == constants.TAG_ACTIVATION_POINT_GENESIS:
        return _decode_activation_point_genesis(bytes_rem)
    else:
        raise ValueError("Invalid type tag: activation point ")


def _decode_activation_point_era_id(bytes_in: bytes) -> typing.Tuple[bytes, ActivationPoint_Era]:
    bytes_rem, era_id = decode(EraID, bytes_in)

    return bytes_rem, ActivationPoint_Era(era_id)


def _decode_activation_point_genesis(bytes_in: bytes) -> typing.Tuple[bytes, ActivationPoint_Genesis]:
    bytes_rem, timestamp = decode(Timestamp, bytes_in)

    return bytes_rem, ActivationPoint_Genesis(timestamp)


def _decode_available_block_range(bytes_in: bytes) -> typing.Tuple[bytes, AvailableBlockRange]:
    bytes_rem, low = decode(U64, bytes_in)
    bytes_rem, high = decode(U64, bytes_rem)

    return bytes_rem, AvailableBlockRange(low, high)


def _decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    bytes_rem, type_tag = decode(U8, bytes_in)
    if type_tag == constants.TAG_BLOCK_TYPE_V1:
        return _decode_block_header_v1(bytes_rem)
    elif type_tag == constants.TAG_BLOCK_TYPE_V2:
        return _decode_block_header_v2(bytes_rem)
    else:
        raise ValueError("Invalid type tag: block header ")


def _decode_block_header_v1(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V1]:
    raise NotImplementedError()


def _decode_block_header_v2(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V2]:
    bytes_rem, parent_block_hash = decode(BlockHash, bytes_in)
    bytes_rem, state_root_hash = decode(DigestBytes, bytes_rem)
    bytes_rem, body_hash = decode(BlockBodyHash, bytes_rem)
    bytes_rem, random_bit = decode(bool, bytes_rem)
    bytes_rem, accumulated_seed = decode(DigestBytes, bytes_rem)
    bytes_rem, era_end = decode(EraEnd_V2, bytes_rem, is_optional=True)
    bytes_rem, timestamp = decode(Timestamp, bytes_rem)
    bytes_rem, era_id = decode(EraID, bytes_rem)
    bytes_rem, height = decode(BlockHeight, bytes_rem)
    bytes_rem, protocol_version = decode(ProtocolVersion, bytes_rem)
    bytes_rem, proposer = decode(PublicKeyBytes, bytes_rem)
    bytes_rem, current_gas_price = decode(GasPrice, bytes_rem)
    bytes_rem, last_switch_block_hash = decode(DigestBytes, bytes_rem, is_optional=True)

    return bytes_rem, BlockHeader_V2(
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


def _decode_block_synchronizer_status(bytes_in: bytes) -> typing.Tuple[bytes, BlockSynchronizerStatus]:
    bytes_rem, historical = decode(BlockSynchronizerStatusInfo, bytes_in, is_optional=True)
    bytes_rem, forward = decode(BlockSynchronizerStatusInfo, bytes_rem, is_optional=True)

    if historical is None and forward is None:
        return bytes_rem, None
    else:
        return bytes_rem, BlockSynchronizerStatus(historical, forward)


def _decode_block_synchronizer_status_info(bytes_in: bytes) -> typing.Tuple[bytes, BlockSynchronizerStatusInfo]:
    bytes_rem, block_hash = decode(BlockHash, bytes_in)
    bytes_rem, block_height = decode(BlockHeight, bytes_rem, is_optional=True)
    bytes_rem, acquisition_state = decode(str, bytes_rem)

    return bytes_rem, BlockSynchronizerStatusInfo(block_hash, block_height, acquisition_state)


def _decode_chainspec_raw_bytes(bytes_in: bytes) -> typing.Tuple[bytes, ChainspecRawBytes]:
    bytes_rem, chainspec_bytes = decode(bytes, bytes_in)
    bytes_rem, genesis_accounts_bytes = decode(bytes, bytes_rem, is_optional=True)
    bytes_rem, global_state_bytes = decode(bytes, bytes_rem, is_optional=True)

    return bytes_rem, ChainspecRawBytes(chainspec_bytes, genesis_accounts_bytes, global_state_bytes)


def _decode_consensus_state(bytes_in: bytes) -> typing.Tuple[bytes, ConsensusStatus]:
    bytes_rem, validator_public_key = decode(PublicKey, bytes_in)
    bytes_rem, round_length = decode(TimeDifference, bytes_rem, is_optional=True)

    return bytes_rem, ConsensusStatus(validator_public_key, round_length)


def _decode_era_end_v1(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V1]:
    raise NotImplementedError()


def _decode_era_end_v2(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V2]:
    bytes_rem, equivocators = decode(ValidatorID, bytes_in, is_sequence=True)
    bytes_rem, inactive_validators = decode(ValidatorID, bytes_rem, is_sequence=True)
    bytes_rem, next_era_validator_weights = decode(EraValidatorWeight, bytes_rem, is_sequence=True)
    bytes_rem, rewards = decode(EraValidatorReward, bytes_rem, is_sequence=True)
    bytes_rem, next_era_gas_price = decode(GasPrice, bytes_rem)

    return bytes_rem, EraEnd_V2(
        equivocators=equivocators,
        inactive_validators=inactive_validators,
        next_era_gas_price=next_era_gas_price,
        next_era_validator_weights=next_era_validator_weights,
        rewards=rewards
    )


def _decode_era_validator_reward(bytes_in: bytes) -> typing.Tuple[bytes, EraValidatorReward]:
    bytes_rem, validator_id = decode(ValidatorID, bytes_in)
    bytes_rem, rewards = decode(Motes, bytes_rem, is_sequence=True)

    return bytes_rem, EraValidatorReward(rewards, validator_id)


def _decode_era_validator_weight(bytes_in: bytes) -> typing.Tuple[bytes, EraValidatorWeight]:
    bytes_rem, validator_id = decode(ValidatorID, bytes_in)
    bytes_rem, weight = decode(Weight, bytes_rem)

    return bytes_rem, EraValidatorWeight(validator_id, weight)


def _decode_next_upgrade(bytes_in: bytes) -> typing.Tuple[bytes, NextUpgrade]:
    bytes_rem, activation_point = decode(ActivationPoint, bytes_in)
    bytes_rem, protocol_version = decode(ProtocolVersion, bytes_rem)

    return bytes_rem, NextUpgrade(activation_point, protocol_version)


def _decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = decode(U32, bytes_in)
    bytes_rem, minor = decode(U32, bytes_rem)
    bytes_rem, patch = decode(U32, bytes_rem)

    return bytes_rem, ProtocolVersion(major, minor, patch)


# Complex types.
register_decoders({
    (ActivationPoint, _decode_activation_point),
    (AvailableBlockRange, _decode_available_block_range),
    (BlockHeader, _decode_block_header),
    (BlockHeader_V1, _decode_block_header_v1),
    (BlockHeader_V2, _decode_block_header_v2),
    (BlockSynchronizerStatus, _decode_block_synchronizer_status),
    (BlockSynchronizerStatusInfo, _decode_block_synchronizer_status_info),
    (ChainspecRawBytes, _decode_chainspec_raw_bytes),
    (ConsensusStatus, _decode_consensus_state),
    (EraEnd_V1, _decode_era_end_v1),
    (EraEnd_V2, _decode_era_end_v2),
    (EraValidatorReward, _decode_era_validator_reward),
    (EraValidatorWeight, _decode_era_validator_weight),
    (NextUpgrade, _decode_next_upgrade),
    (ProtocolVersion, _decode_protocol_version),
    (ValidatorID, lambda x: decode(PublicKey, x)),
})
