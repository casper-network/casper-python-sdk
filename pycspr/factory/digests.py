import operator

from pycspr import crypto
from pycspr import serialisation
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
    account = CL_PublicKey.from_key(header.account_public_key)
    timestamp = CL_U64(int(header.timestamp.value * 1000))
    ttl = CL_U64(header.ttl.as_milliseconds)
    gas_price = CL_U64(header.gas_price)
    body_hash = CL_ByteArray(header.body_hash)
    dependencies = CL_List(header.dependencies, CL_Type_String())
    chain_name = CL_String(header.chain_name)

    return crypto.get_hash(
        serialisation.cl_value_to_bytes(account) +
        serialisation.cl_value_to_bytes(timestamp) +
        serialisation.cl_value_to_bytes(ttl) +
        serialisation.cl_value_to_bytes(gas_price) +
        serialisation.cl_value_to_bytes(body_hash) +
        serialisation.cl_value_to_bytes(dependencies) +
        serialisation.cl_value_to_bytes(chain_name)
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
        serialisation.deploy_to_bytes(payment) +
        serialisation.deploy_to_bytes(session)
        )
