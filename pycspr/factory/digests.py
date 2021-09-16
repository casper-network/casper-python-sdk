import typing

from pycspr import crypto
from pycspr import factory
from pycspr import serialisation
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
        factory.create_cl_type_of_list(factory.create_cl_type_of_simple(CLTypeKey.STRING)),
        header.dependencies
    )

    # Element 7: chain-name. 
    cl_chain_name = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.STRING),
        header.chain_name
    )

    return crypto.get_hash(
        serialisation.to_bytes(cl_account) + \
        serialisation.to_bytes(cl_timestamp) + \
        serialisation.to_bytes(cl_ttl) + \
        serialisation.to_bytes(cl_gas_price) + \
        serialisation.to_bytes(cl_body_hash) + \
        serialisation.to_bytes(cl_dependencies) + \
        serialisation.to_bytes(cl_chain_name)
        )


def create_digest_of_deploy_body(
    payment: ExecutableDeployItem,
    session: ExecutableDeployItem
    ) -> bytes:
    """Returns a deploy body's hash digest.
    
    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hash digest of a deploy body.

    """   
    return crypto.get_hash(
        serialisation.to_bytes(payment) + \
        serialisation.to_bytes(session)
        )
