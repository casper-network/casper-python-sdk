import typing

from pycspr import factory
from pycspr import codec
from pycspr import crypto
from pycspr.types import CLTypeKey
from pycspr.types import ExecutionInfo
from pycspr.types import DeployHeader



def create_digest_of_deploy(header: DeployHeader) -> bytes:
    """Returns a deploy's hash digest.
    
    :param header: Deploy header information.
    :returns: Hash digest of a deploy.

    """
    # Element 1: account. 
    cl_account = factory.create_cl_value(
        factory.create_cl_type_of_simple(CLTypeKey.PUBLIC_KEY),
        header.accountPublicKey
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
        codec.to_bytes(cl_account) + \
        codec.to_bytes(cl_timestamp) + \
        codec.to_bytes(cl_ttl) + \
        codec.to_bytes(cl_gas_price) + \
        codec.to_bytes(cl_body_hash) + \
        codec.to_bytes(cl_dependencies) + \
        codec.to_bytes(cl_chain_name)
        )


def create_digest_of_deploy_body(payment: ExecutionInfo, session: ExecutionInfo) -> bytes:
    """Returns a deploy body's hash digest.
    
    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hash digest of a deploy body.

    """    
    return crypto.get_hash(
        codec.to_bytes(payment) + \
        codec.to_bytes(session)
        )
