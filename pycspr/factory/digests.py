from pycspr import crypto
from pycspr import serializer
from pycspr.types.node.rpc import DeployHeader
from pycspr.types.cl import CLV_ByteArray
from pycspr.types.cl import CLV_List
from pycspr.types.cl import CLV_String
from pycspr.types.cl import CLV_U64
from pycspr.types.node.rpc import DeployExecutableItem
from pycspr.utils import convertor


def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.

    :param header: Deploy header information.
    :returns: Hash digest of a deploy.

    """
    return crypto.get_hash(
        serializer.to_bytes(
            convertor.clv_public_key_from_public_key(header.account)
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
