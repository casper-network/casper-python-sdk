from pycspr import crypto
from pycspr import factory
from pycspr.serialisation import to_bytes
from pycspr.types import CLTypeKey
from pycspr.types import ExecutableDeployItem
from pycspr.types import DeployHeader


def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.
    :param header: Deploy header information.
    :returns: Hash digest of a deploy.
    """
    # Element 1: account.
    cl_account = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY),
        header.account_public_key
    )

    # Element 2: timestamp.
    cl_timestamp = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.U64),
        int(header.timestamp * 1000)
    )

    # Element 3: ttl.
    cl_ttl = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.U64),
        header.ttl.as_milliseconds
    )

    # Element 4: gas-price.
    cl_gas_price = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.U64),
        header.gas_price
    )

    # Element 5: body-hash.
    cl_body_hash = factory.create_cl_value(
        factory.create_cl_type_of_byte_array(32),
        header.body_hash
    )

    # Element 6: dependencies.
    cl_dependencies = factory.create_cl_value(
        factory.create_cl_type_of_list(
            factory.create_cl_type_of_simple(CLTypeKey.STRING)
        ),
        header.dependencies
    )

    # Element 7: chain-name.
    cl_chain_name = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.STRING),
        header.chain_name
    )

    digest_list = [to_bytes(cl_timestamp),
                   to_bytes(cl_ttl), to_bytes(cl_gas_price),
                   to_bytes(cl_body_hash), to_bytes(cl_dependencies),
                   to_bytes(cl_chain_name)]
    digest_sum = to_bytes(cl_account)
    for b in digest_list:
        digest_sum += b
    return crypto.get_hash(digest_sum)


def create_digest_of_deploy_body(payment: ExecutableDeployItem,
                                 session: ExecutableDeployItem
                                 ) -> bytes:
    """Returns a deploy body's hash digest.
    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hash digest of a deploy body.
    """
    return crypto.get_hash(to_bytes(payment) + to_bytes(session))
