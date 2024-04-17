from pycspr import crypto
from pycspr import serializer
from pycspr.types.cl import CLV_Bool
from pycspr.types.cl import CLV_ByteArray
from pycspr.types.cl import CLV_List
from pycspr.types.cl import CLV_Option
from pycspr.types.cl import CLV_PublicKey
from pycspr.types.cl import CLV_String
from pycspr.types.cl import CLV_U64
from pycspr.types.cl import CLT_ByteArray
from pycspr.types.node.rpc import BlockHeader
from pycspr.types.node.rpc import DeployExecutableItem
from pycspr.types.node.rpc import DeployHeader


def create_digest_of_block(header: BlockHeader) -> bytes:
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


def create_digest_of_deploy(header: DeployHeader) -> bytes:
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
) -> bytes:
    """Returns a deploy body's hash digest.

    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hash digest of a deploy body.

    """
    return crypto.get_hash(
        serializer.to_bytes(payment) +
        serializer.to_bytes(session)
        )
