from __future__ import annotations

import dataclasses
import enum
import typing

from pycspr.type_defs.crypto import \
    DigestBytes, \
    PublicKey, \
    PublicKeyBytes, \
    Signature
from pycspr.type_defs.primitives import \
    U64, \
    TimeDifference, \
    Timestamp


GasPrice = typing.NewType(
    "Multiplier applied to estimation of computational costs (gas).", int
)

TransactionBodyHash = typing.NewType(
    "Digest over a transaction body.", DigestBytes
    )

TransactionHash = typing.NewType(
    "Digest over a transaction.", DigestBytes
    )

TransactionInitiatorAddress = typing.NewType(
    "Initiating address of a tx creator.", typing.Union[DigestBytes, PublicKey]
    )


@dataclasses.dataclass
class PricingMode():
    """Mode of tx execution pricing.

    """
    pass


@dataclasses.dataclass
class PricingMode_Classic(PricingMode):
    """Mode of tx execution pricing: tx creator specifies a gas limit & price.

    """
    # User-specified payment amount.
    payment_amount: int

    # User-specified gas_price tolerance (minimum 1).
    gas_price_tolerance: int

    # Flag indicating whether to utilise standard payment.
    standard_payment: bool = True


@dataclasses.dataclass
class PricingMode_Fixed(PricingMode):
    """Mode of tx execution pricing: determined by cost table as per tx category.

    """
    # User-specified gas_price tolerance (minimum 1).
    gas_price_tolerance: int


@dataclasses.dataclass
class PricingMode_Reserved(PricingMode):
    """Mode of tx execution pricing: tx payment was previously reserved.

    """
    # Pre-paid receipt.
    receipt: DigestBytes


@dataclasses.dataclass
class Transaction():
    """Transaction dispatched into and processed by network.

    """
    pass


@dataclasses.dataclass
class Transaction_V1():
    """Transaction version one.

    """
    pass


@dataclasses.dataclass
class Transaction_V2():
    """Transaction version two.

    """
    # Digest over tx contents.
    hash: TransactionHash

    # Header information.
    header: Transaction_V2_Header

    # body: TransactionV1Body,
    # approvals: BTreeSet<Approval>,


@dataclasses.dataclass
class Transaction_V2_Header():
    """Transaction version one header.

    """
    # Name of chain to which tx has been dispatched.
    chain_name: str

    # Instantiation timestamp.
    timestamp: Timestamp

    # Time period after which tx will no longer be processed.
    ttl: TimeDifference

    # Digest over tx body.
    body_hash: TransactionBodyHash

    # Mode of pricing to apply.
    pricing_mode: PricingMode

    # On-chain address of tx intiator.
    initiator_address: TransactionInitiatorAddress
