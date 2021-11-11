from pycspr import crypto
from pycspr import serialisation
from pycspr.factory import cl_type as cl_type_factory
from pycspr.factory import cl_value as cl_value_factory
from pycspr.types import DeployExecutableItem
from pycspr.types import DeployHeader


def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.

    :param header: Deploy header information.
    :returns: Hash digest of a deploy.

    """
    # Element 1: account.
    account = cl_value_factory.public_key(header.account_public_key)

    # Element 2: timestamp.
    timestamp = cl_value_factory.u64(int(header.timestamp * 1000))

    # Element 3: ttl.
    ttl = cl_value_factory.u64(header.ttl.as_milliseconds)

    # Element 4: gas-price.
    gas_price = cl_value_factory.u64(header.gas_price)

    # Element 5: body-hash.
    body_hash = cl_value_factory.byte_array(header.body_hash)

    # Element 6: dependencies.
    dependencies = cl_value_factory.list(cl_type_factory.string(), header.dependencies)

    # Element 7: chain-name.
    chain_name = cl_value_factory.string(header.chain_name)

    return crypto.get_hash(
        serialisation.to_bytes(account) +
        serialisation.to_bytes(timestamp) +
        serialisation.to_bytes(ttl) +
        serialisation.to_bytes(gas_price) +
        serialisation.to_bytes(body_hash) +
        serialisation.to_bytes(dependencies) +
        serialisation.to_bytes(chain_name)
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
