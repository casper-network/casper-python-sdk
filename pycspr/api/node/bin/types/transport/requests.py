import dataclasses
import typing

from pycspr.api.node.bin.types.primitives.crypto import PublicKeyBytes
from pycspr.api.node.bin.types.chain import \
    BlockID, \
    EraID, \
    TransactionHash


@dataclasses.dataclass
class Get_Information_BlockHeader_RequestPayload():
    """Request payload: Get.Information.BlockHeader endpoint.

    """
    block_id: typing.Optional[BlockID]


@dataclasses.dataclass
class Get_Information_Reward_RequestPayload():
    """Request payload: Get.Information.Reward endpoint.

    """
    delegator: typing.Optional[PublicKeyBytes]
    era_id: typing.Optional[EraID]
    validator: PublicKeyBytes


@dataclasses.dataclass
class Get_Information_SignedBlock_RequestPayload():
    """Request payload: Get.Information.SignedBlock endpoint.

    """
    block_id: typing.Optional[BlockID]


@dataclasses.dataclass
class Get_Information_Transaction_RequestPayload():
    """Request payload: Get.Information.Transaction endpoint.

    """
    # Hash of the transaction to retrieve.
    hash: TransactionHash

    # Whether to return the deploy with the finalized approvals substituted.
    with_finalized_approvals: bool
