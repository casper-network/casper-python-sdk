import typing

from pycspr import crypto
from pycspr import serialisation
from pycspr.types import CL_Bool
from pycspr.types import CL_ByteArray
from pycspr.types import CL_List
from pycspr.types import CL_PublicKey
from pycspr.types import CL_String
from pycspr.types import CL_U64
from pycspr.utils.conversion import isoformat_from_posix_timestamp

from pycspr.litmus.types import Block
from pycspr.litmus.types import BlockBody
from pycspr.litmus.types import BlockHeader
from pycspr.litmus.types import BlockHeight
from pycspr.litmus.types import BlockSignature
from pycspr.litmus.types import Digest
from pycspr.litmus.types import SemanticVersion


def get_digest_of_block(header: BlockHeader) -> Digest:
    # N.B. order matters !

    return crypto.get_hash(
        serialisation.to_bytes(
            CL_ByteArray(header.parent_hash)
        ) +
        serialisation.to_bytes(
            CL_ByteArray(header.state_root_hash)
        ) +
        serialisation.to_bytes(
            CL_ByteArray(header.body_hash)
        ) +
        serialisation.to_bytes(
            CL_Bool(header.random_bit)
        ) +
        serialisation.to_bytes(
            CL_ByteArray(header.accumulated_seed)
        ) +
        serialisation.to_bytes(
            CL_U64(header.era_id)
        ) +
        serialisation.to_bytes(
            CL_U64(int(header.timestamp.value * 1000))
        ) +
        serialisation.to_bytes(
            CL_U64(header.height)
        ) +
        serialisation.to_bytes(
            header.protocol_version
        )
    )

        # serialisation.to_bytes(
        #     CL_U64(header.era_end)
        # ) +


# @dataclasses.dataclass
# class BlockHeader:
#      accumulated_seed: Digest
#      body_hash: Digest
#     era_end: typing.Optional[EraEnd]
#      era_id: EraId
#      height: BlockHeight
#      parent_hash: BlockHash
#     protocol_version: SemanticVersion
#      random_bit: bool
#      state_root_hash: Digest
#     timestamp: Timestamp


# let mut buffer = casper_types::bytesrepr::allocate_buffer(self)?;
# buffer.extend(self.parent_hash.to_bytes()?);
# buffer.extend(self.state_root_hash.to_bytes()?);
# buffer.extend(self.body_hash.to_bytes()?);
# buffer.extend(self.random_bit.to_bytes()?);
# buffer.extend(self.accumulated_seed.to_bytes()?);
# buffer.extend(self.era_end.to_bytes()?);
# buffer.extend(self.timestamp.to_bytes()?);
# buffer.extend(self.era_id.to_bytes()?);
# buffer.extend(self.height.to_bytes()?);
# buffer.extend(self.protocol_version.to_bytes()?);
# Ok(buffer)


# return crypto.get_hash(
#     serialisation.to_bytes(
#         CL_PublicKey.from_public_key(header.account_public_key)
#     ) +
#     serialisation.to_bytes(
#         CL_U64(int(header.timestamp.value * 1000))
#     ) +
#     serialisation.to_bytes(
#         CL_U64(header.ttl.as_milliseconds)
#     ) +
#     serialisation.to_bytes(
#         CL_U64(header.gas_price)
#     ) +
#     serialisation.to_bytes(
#         CL_ByteArray(header.body_hash)
#     ) +
#     serialisation.to_bytes(
#         CL_List(header.dependencies)
#     ) +
#     serialisation.to_bytes(
#         CL_String(header.chain_name)
#     )
# )


def encode_semantic_version(entity: SemanticVersion) -> bytes:
    return \
        serialisation.to_bytes(CL_U64(entity.major)) + \
        serialisation.to_bytes(CL_U64(entity.minor)) + \
        serialisation.to_bytes(CL_U64(entity.patch))
