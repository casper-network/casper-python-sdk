from pycspr import crypto
from pycspr import serializer
from pycspr.type_defs.cl_values import CLV_Bool
from pycspr.type_defs.cl_values import CLV_ByteArray
from pycspr.type_defs.cl_values import CLV_List
from pycspr.type_defs.cl_values import CLV_Option
from pycspr.type_defs.cl_values import CLV_PublicKey
from pycspr.type_defs.cl_values import CLV_String
from pycspr.type_defs.cl_values import CLV_U64
from pycspr.type_defs.cl_types import CLT_ByteArray
from pycspr.type_defs.crypto import DigestBytes
from pycspr.types.node import Block
from pycspr.types.node import BlockHeader
from pycspr.types.node import DeployExecutableItem
from pycspr.types.node import DeployHeader


def create_digest_of_block(header: BlockHeader) -> DigestBytes:
    """Returns a block's digest.

    :param header: Block header information.
    :returns: Digest of a block.

    """
    return crypto.get_hash(
        serializer.to_bytes(
            CLV_ByteArray(
                header.parent_hash
            )
        ) +
        serializer.to_bytes(
            CLV_ByteArray(
                header.state_root
            )
        ) +
        serializer.to_bytes(
            CLV_ByteArray(
                header.body_hash
            )
        ) +
        serializer.to_bytes(
            CLV_Bool(
                header.random_bit
            )
        ) +
        serializer.to_bytes(
            CLV_ByteArray(
                header.accumulated_seed
            )
        ) +
        serializer.to_bytes(
            CLV_Option(
                CLV_ByteArray(
                    serializer.to_bytes(header.era_end)
                ),
                CLT_ByteArray
            )
        ) +
        serializer.to_bytes(
            CLV_U64(
                int(header.timestamp.value * 1000)
            )
        ) +
        serializer.to_bytes(
            CLV_U64(
                header.era_id
            )
        ) +
        serializer.to_bytes(
            CLV_U64(
                header.height
            )
        ) +
        serializer.to_bytes(
            header.protocol_version
        )
    )


def create_digest_of_block_for_finality_signature(block: Block) -> DigestBytes:
    return block.hash + serializer.to_bytes(
        CLV_U64(block.header.era_id)
    )


def create_digest_of_deploy(header: DeployHeader) -> DigestBytes:
    """Returns a deploy's digest.

    :param header: Deploy header information.
    :returns: Digestigest of a deploy.

    """
    return crypto.get_hash(
        serializer.to_bytes(
            CLV_PublicKey.from_public_key(header.account)
        ) +
        serializer.to_bytes(
            CLV_U64(int(header.timestamp.value * 1000))
        ) +
        serializer.to_bytes(
            CLV_U64(header.ttl.as_milliseconds)
        ) +
        serializer.to_bytes(
            CLV_U64(header.gas_price)
        ) +
        serializer.to_bytes(
            CLV_ByteArray(header.body_hash)
        ) +
        serializer.to_bytes(
            CLV_List(header.dependencies)
        ) +
        serializer.to_bytes(
            CLV_String(header.chain_name)
        )
    )


def create_digest_of_deploy_body(
    payment: DeployExecutableItem,
    session: DeployExecutableItem
) -> DigestBytes:
    """Returns a deploy body's hash digest.

    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hash digest of a deploy body.

    """
    return crypto.get_hash(
        serializer.to_bytes(payment) +
        serializer.to_bytes(session)
        )
