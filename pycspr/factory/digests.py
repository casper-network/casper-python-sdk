from pycspr import crypto
from pycspr import serialisation
from pycspr.types.rpc import DeployHeader
from pycspr.types.cl import CLV_ByteArray
from pycspr.types.cl import CLV_List
from pycspr.types.cl import CLV_PublicKey
from pycspr.types.cl import CLV_String
from pycspr.types.cl import CLV_U64
from pycspr.types.rpc import DeployExecutableItem


def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.

    :param header: Deploy header information.
    :returns: Hash digest of a deploy.

    """
    return crypto.get_hash(
        serialisation.to_bytes(
            CLV_PublicKey.from_public_key(header.account)
        ) +
        serialisation.to_bytes(
            CLV_U64(int(header.timestamp.value * 1000))
        ) +
        serialisation.to_bytes(
            CLV_U64(header.ttl.as_milliseconds)
        ) +
        serialisation.to_bytes(
            CLV_U64(header.gas_price)
        ) +
        serialisation.to_bytes(
            CLV_ByteArray(header.body_hash)
        ) +
        serialisation.to_bytes(
            CLV_List(header.dependencies)
        ) +
        serialisation.to_bytes(
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
        serialisation.to_bytes(payment) +
        serialisation.to_bytes(session)
        )
