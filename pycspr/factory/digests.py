from pycspr import crypto
from pycspr import serialisation1
from pycspr.types import CL_PublicKey
from pycspr.types import CL_U64
from pycspr.types import CL_ByteArray
from pycspr.types import CL_List
from pycspr.types import CL_String
from pycspr.types import DeployExecutableItem
from pycspr.types import DeployHeader


def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.

    :param header: Deploy header information.
    :returns: Hash digest of a deploy.

    """
    return crypto.get_hash(
        serialisation1.to_bytes(
            CL_PublicKey.from_public_key(header.account_public_key)
        ) +
        serialisation1.to_bytes(
            CL_U64(int(header.timestamp.value * 1000))
        ) +
        serialisation1.to_bytes(
            CL_U64(header.ttl.as_milliseconds)
        ) +
        serialisation1.to_bytes(
             CL_U64(header.gas_price)
        ) +
        serialisation1.to_bytes(
            CL_ByteArray(header.body_hash)
        ) +
        serialisation1.to_bytes(
            CL_List(header.dependencies)
        ) +
        serialisation1.to_bytes(
            CL_String(header.chain_name)
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
        serialisation1.to_bytes(payment) +
        serialisation1.to_bytes(session)
        )
