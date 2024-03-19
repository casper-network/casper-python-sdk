from __future__ import annotations

import dataclasses
import typing


BlockHash = typing.NewType("Cryptographically derived identifier of a block.", "Digest")

BlockHeight = typing.NewType("A specific location in a blockchain, measured by how many finalised blocks precede it.", int)

DeployHash = typing.NewType("Cryptographically derived identifier of a deploy.", "Digest")

Digest = typing.NewType("Cryptographic fingerprint of data.", bytes)

EraID = typing.NewType("Identifier of an era in chain time.", int)

Motes = typing.NewType("Basic unit of crypto economic system.", int)

PublicKey = typing.NewType("Asymmetric public key associated with an account.", bytes)

Signature = typing.NewType("Cryptographic signature over data.", bytes)

Weight = typing.NewType("Some form of relative relevance measure.", int)


@dataclasses.dataclass
class Block:
    hash: Digest
    header: typing.Optional[BlockHeader]
    body: BlockBody
    proofs: typing.List[BlockSignature]


@dataclasses.dataclass
class BlockBody:
    proposer: PublicKey
    deploy_hashes: typing.List[DeployHash]
    transfer_hashes: typing.List[DeployHash]


@dataclasses.dataclass
class BlockHeader:
    accumulated_seed: Digest
    body_hash: Digest
    era_end: typing.Optional[EraEnd]
    era_id: EraId
    height: BlockHeight
    parent_hash: BlockHash
    protocol_version: SemanticVersion
    random_bit: bool
    state_root_hash: Digest
    timestamp: Timestamp


@dataclasses.dataclass
class BlockSignature():
    public_key: PublicKey
    signature: Signature


@dataclasses.dataclass
class BlockSignatures:
    block_hash: BlockHash
    era_id: EraId
    proofs: typing.Dict[PublicKey, BlockSignature]


@dataclasses.dataclass
class BlockHeaderWithSignatures:
    header: BlockHeader
    signatures: BlockSignatures


@dataclasses.dataclass
class EraEnd:
    era_report: EraReport
    next_era_validator_weights: typing.List[ValidatorWeight]


@dataclasses.dataclass
class EraInfo:
    era_id: EraId
    validator_weights: typing.List[ValidatorWeight]
    total_weight: Weight


@dataclasses.dataclass
class EraReport:
    equivocators: typing.List[PublicKey]
    rewards: typing.List[EraReward]
    inactive_validators: typing.List[PublicKey]


@dataclasses.dataclass
class EraReward:
    validator: PublicKey
    amount: Motes


@dataclasses.dataclass
class SemanticVersion:
    major : int
    minor : int
    patch : int


@dataclasses.dataclass
class Timestamp():
    value: float


@dataclasses.dataclass
class ValidatorWeight():
    validator: PublicKey
    weight: Weight
