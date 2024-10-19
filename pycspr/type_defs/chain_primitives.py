from __future__ import annotations

import typing

from pycspr.type_defs.crypto import DigestBytes, PublicKey
from pycspr.type_defs.primitives import U64


AccountAddressBytes = typing.NewType(
    "Byte representation of an on chain address of an account mapped from an EOA public key.", bytes
    )


AccountKeyBytes = typing.NewType(
    "Byte representation of an account key.", bytes
    )


BlockBodyHash = typing.NewType(
    "Digest over a block's body.", DigestBytes
    )

BlockHash = typing.NewType(
    "Digest over a block.", DigestBytes
    )

BlockHeight = typing.NewType(
    "Ordinal identifier of a block measured by how many finalised blocks precede it.", U64
)

BlockID = typing.Union[BlockHash, BlockHeight]

ChainNameDigest = typing.NewType(
    "Digest over a network's chain name.", DigestBytes
    )

DelegationRate = typing.NewType(
    "Delegation rate of tokens. Range from 0..=100.", int
    )

EraID = typing.NewType(
    "Ordinal identifier of an era measured by how many eras precede it.", int
)

GasPrice = typing.NewType(
    "Multiplier applied to estimation of computational costs (gas).", int
)

Motes = typing.NewType(
    "Basic unit of crypto economic system.", int
    )

StateRootHash = typing.NewType(
    "Root digest of a node's global state.", DigestBytes
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

Weight = typing.NewType(
    "Some form of relative relevance measure.", int
    )
