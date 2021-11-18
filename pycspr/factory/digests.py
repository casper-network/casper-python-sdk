from pycspr import crypto
from pycspr.types import CL_PublicKey
from pycspr.types import CL_U64
from pycspr.types import CL_ByteArray
from pycspr.types import CL_List
from pycspr.types import CL_String
from pycspr.types import CL_Type_String
from pycspr.types import DeployExecutableItem
from pycspr.types import DeployHeader


def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.

    :param header: Deploy header information.
    :returns: Hash digest of a deploy.

    """
    return crypto.get_hash(
        CL_PublicKey.from_key(header.account_public_key).to_bytes() +
        CL_U64(int(header.timestamp * 1000)).to_bytes() +
        CL_U64(header.ttl.as_milliseconds).to_bytes() +
        CL_U64(header.gas_price).to_bytes() +
        CL_ByteArray(header.body_hash).to_bytes() +
        CL_List(header.dependencies, CL_Type_String()).to_bytes() +
        CL_String(header.chain_name).to_bytes()
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
        payment.to_bytes() +
        session.to_bytes()
        )
