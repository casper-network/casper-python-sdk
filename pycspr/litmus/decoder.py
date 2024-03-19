import typing

from pycspr.litmus.types import Block
from pycspr.litmus.types import BlockBody
from pycspr.litmus.types import BlockHeader
from pycspr.litmus.types import BlockHeight
from pycspr.litmus.types import BlockSignature
from pycspr.litmus.types import Digest
from pycspr.litmus.types import EraEnd  
from pycspr.litmus.types import EraID
from pycspr.litmus.types import EraReport
from pycspr.litmus.types import EraReward
from pycspr.litmus.types import Motes
from pycspr.litmus.types import PublicKey
from pycspr.litmus.types import SemanticVersion
from pycspr.litmus.types import Signature
from pycspr.litmus.types import Timestamp
from pycspr.litmus.types import ValidatorWeight
from pycspr.litmus.types import Weight
from pycspr.utils import conversion


def decode(typedef: type, encoded: dict) -> typing.Optional[object]:
    if encoded is not None:
        try:
            decoder = _DECODERS[typedef]
        except KeyError:
            raise ValueError(f"Cannot decode {typedef} from json object")
        else:
            return decoder(encoded)


def _decode_block(encoded: dict) -> Block:
    return Block(
        body=decode(BlockBody, encoded["body"]),
        hash=decode(Digest, encoded["hash"]),
        header=decode(BlockHeader, encoded["header"]),
        proofs=[decode(BlockSignature, i) for i in encoded["proofs"]],
    )


def _decode_block_body(encoded: dict) -> BlockBody:
    return BlockBody(
        proposer=decode(PublicKey, encoded["proposer"]),
        deploy_hashes=[decode(Digest, i) for i in encoded["deploy_hashes"]],
        transfer_hashes=[decode(Digest, i) for i in encoded["transfer_hashes"]],
    )


def _decode_block_header(encoded: dict) -> BlockHeader:
    return BlockHeader(
        accumulated_seed=decode(Digest, encoded["accumulated_seed"]),
        body_hash=decode(Digest, encoded["body_hash"]),
        era_end=decode(EraEnd, encoded.get("era_end")),
        era_id=decode(EraID, encoded["era_id"]),
        height=decode(BlockHeight, encoded["height"]),
        parent_hash=decode(Digest, encoded["parent_hash"]),
        protocol_version=decode(SemanticVersion, encoded["protocol_version"]),
        random_bit=decode(bool, encoded["random_bit"]),
        state_root_hash=decode(Digest, encoded["state_root_hash"]),
        timestamp=decode(Timestamp, encoded["timestamp"]),
    )


def _decode_block_signature(encoded: dict) -> BlockSignature:
    return BlockSignature(
        public_key=decode(PublicKey, encoded["public_key"]),
        signature=decode(Signature, encoded["signature"]),
    )


def _decode_era_end(encoded: dict) -> EraEnd:
    return EraEnd(
        era_report=decode(EraReport, encoded["era_report"]),
        next_era_validator_weights=[decode(ValidatorWeight, i) for i in encoded["next_era_validator_weights"]]
    )


def _decode_era_report(encoded: dict) -> EraReport:
    return EraReport(
        equivocators=[decode(PublicKey, i) for i in encoded["equivocators"]],
        rewards=[decode(EraReward, i) for i in encoded["rewards"]],
        inactive_validators=[decode(PublicKey, i) for i in encoded["inactive_validators"]],
    )


def _decode_era_reward(encoded: dict) -> EraReward:
    return EraReward(
        validator=decode(PublicKey, encoded["validator"]),
        amount=decode(Motes, encoded["amount"]),
    )

def _decode_semantic_version(encoded: dict) -> SemanticVersion:
    major, minor, patch = encoded.split(".")

    return SemanticVersion(
        major=int(major),
        minor=int(minor),
        patch=int(patch)
        )


def _decode_timestamp(encoded: dict) -> Timestamp:
    return Timestamp(
        value=conversion.posix_timestamp_from_isoformat(encoded)
    )

def _decode_validator_weight(encoded: dict) -> ValidatorWeight:
    return ValidatorWeight(
        validator=decode(PublicKey, encoded["validator"]),
        weight=decode(Weight, encoded["weight"]),
    )


_DECODERS = {
    bool: bool,
    bytes: lambda x: bytes.fromhex(x),
    int: int,
} | {
    BlockHeight: lambda x: decode(int, x),
    Digest: lambda x: decode(bytes, x),
    EraID: lambda x: decode(int, x),
    Motes: lambda x: decode(int, x),
    PublicKey: lambda x: decode(bytes, x),
    Signature: lambda x: decode(bytes, x),
    Weight: lambda x: decode(int, x),
} | {
    Block: _decode_block,
    BlockBody: _decode_block_body,
    BlockHeader: _decode_block_header,
    BlockSignature: _decode_block_signature,
    EraEnd: _decode_era_end,
    EraReport: _decode_era_report,
    EraReward: _decode_era_reward,
    SemanticVersion: _decode_semantic_version,
    Timestamp: _decode_timestamp,
    ValidatorWeight: _decode_validator_weight
}
