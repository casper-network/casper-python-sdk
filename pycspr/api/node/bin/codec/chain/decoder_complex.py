import typing

from pycspr.api.node.bin.codec.utils import decode, register_decoders
from pycspr.api.node.bin.codec.chain import constants
from pycspr.api.node.bin.types.chain.complex import \
    BlockHeader, \
    BlockHeader_V1, \
    BlockHeader_V2, \
    EraEnd, \
    EraEnd_V1, \
    EraEnd_V2, \
    EraValidatorReward, \
    EraValidatorWeight, \
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
from pycspr.api.node.bin.types.primitives.time import Timestamp


def decode_block_header(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader]:
    bytes_rem, type_tag = decode(bytes_in, U8)
    if type_tag == constants.TAG_BLOCK_TYPE_V1:
        return decode_block_header_v1(bytes_rem)
    elif type_tag == constants.TAG_BLOCK_TYPE_V2:
        return decode_block_header_v2(bytes_rem)
    else:
        raise ValueError("Invalid type tag: block header ")


def decode_block_header_v1(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V1]:
    raise NotImplementedError()


def decode_block_header_v2(bytes_in: bytes) -> typing.Tuple[bytes, BlockHeader_V2]:
    bytes_rem, parent_block_hash = decode(bytes_in, BlockHash)
    bytes_rem, state_root_hash = decode(bytes_rem, DigestBytes)
    bytes_rem, body_hash = decode(bytes_rem, BlockBodyHash)
    bytes_rem, random_bit = decode(bytes_rem, bool)
    bytes_rem, accumulated_seed = decode(bytes_rem, DigestBytes)
    bytes_rem, era_end = decode(bytes_rem, EraEnd_V2, is_optional=True)
    bytes_rem, timestamp = decode(bytes_rem, Timestamp)
    bytes_rem, era_id = decode(bytes_rem, EraID)
    bytes_rem, height = decode(bytes_rem, BlockHeight)
    bytes_rem, protocol_version = decode(bytes_rem, ProtocolVersion)
    bytes_rem, proposer = decode(bytes_rem, PublicKeyBytes)
    bytes_rem, current_gas_price = decode(bytes_rem, GasPrice)
    bytes_rem, last_switch_block_hash = decode(bytes_rem, DigestBytes, is_optional=True)

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


def decode_era_end_v1(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V1]:
    raise NotImplementedError()


def decode_era_end_v2(bytes_in: bytes) -> typing.Tuple[bytes, EraEnd_V2]:
    bytes_rem, equivocators = decode(bytes_in, ValidatorID, is_sequence=True)
    bytes_rem, inactive_validators = decode(bytes_rem, ValidatorID, is_sequence=True)
    bytes_rem, next_era_validator_weights = decode(bytes_rem, EraValidatorWeight, is_sequence=True)
    bytes_rem, rewards = decode(bytes_rem, EraValidatorReward, is_sequence=True)
    bytes_rem, next_era_gas_price = decode(bytes_rem, GasPrice)

    return bytes_rem, EraEnd_V2(
        equivocators=equivocators,
        inactive_validators=inactive_validators,
        next_era_gas_price=next_era_gas_price,
        next_era_validator_weights=next_era_validator_weights,
        rewards=rewards
    )


def decode_era_validator_reward(bytes_in: bytes) -> typing.Tuple[bytes, EraValidatorReward]:
    bytes_rem, validator_id = decode(bytes_in, ValidatorID)
    bytes_rem, rewards = decode(bytes_rem, Motes, is_sequence=True)

    return bytes_rem, EraValidatorReward(rewards, validator_id)


def decode_era_validator_weight(bytes_in: bytes) -> typing.Tuple[bytes, EraValidatorWeight]:
    bytes_rem, validator_id = decode(bytes_in, ValidatorID)
    bytes_rem, weight = decode(bytes_rem, Weight)

    return bytes_rem, EraValidatorWeight(validator_id, weight)


def decode_protocol_version(bytes_in: bytes) -> typing.Tuple[bytes, ProtocolVersion]:
    bytes_rem, major = decode(bytes_in, U32)
    bytes_rem, minor = decode(bytes_rem, U32)
    bytes_rem, patch = decode(bytes_rem, U32)

    return bytes_rem, ProtocolVersion(major, minor, patch)


# Complex types.
register_decoders({
    (BlockHeader, decode_block_header),
    (BlockHeader_V1, decode_block_header_v1),
    (BlockHeader_V2, decode_block_header_v2),
    (EraEnd_V1, decode_era_end_v1),
    (EraEnd_V2, decode_era_end_v2),
    (EraValidatorReward, decode_era_validator_reward),
    (EraValidatorWeight, decode_era_validator_weight),
    (ProtocolVersion, decode_protocol_version),
    (ValidatorID, lambda x: decode(x, PublicKey)),
})
