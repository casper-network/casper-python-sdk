import typing

from pycspr import factory
from pycspr import codec
from pycspr import crypto
from pycspr.types.cl import CLTypeKey
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import DeployHeader



def get_digest_of_deploy(
    header: DeployHeader,
    encoding=crypto.HashEncoding.HEX
    ) -> typing.Union[str, bytes, typing.List[int]]:
    """Returns a deploy's digest.
    
    :param header: Deploy header information.
    :returns: Hexademcimal string representation of a deploy digest.

    """
    # Element 1: account. 
    cl_account = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.PUBLIC_KEY),
        header.accountPublicKey
    )

    # Element 2: timestamp. 
    cl_timestamp = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.U64),
        int(header.timestamp * 1000)
    )

    # Element 3: ttl. 
    cl_ttl = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.U64),
        header.ttl.as_milliseconds
    )

    # Element 4: gas-price. 
    cl_gas_price = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.U64),
        header.gas_price
    )

    # Element 5: body-hash. 
    cl_body_hash = factory.cl.create_value(
        factory.cl.create_byte_array(32),
        header.body_hash
    )

    # Element 6: dependencies. 
    cl_dependencies = factory.cl.create_value(
        factory.cl.create_list(factory.cl.create_simple(CLTypeKey.STRING)),
        header.dependencies
    )

    # Element 7: chain-name. 
    cl_chain_name = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.STRING),
        header.chain_name
    )

    # Set data to be hashed.
    data = \
        codec.to_bytes(cl_account) + \
        codec.to_bytes(cl_timestamp) + \
        codec.to_bytes(cl_ttl) + \
        codec.to_bytes(cl_gas_price) + \
        codec.to_bytes(cl_body_hash) + \
        codec.to_bytes(cl_dependencies) + \
        codec.to_bytes(cl_chain_name)

    return crypto.get_hash(data, encoding=encoding)


def get_digest_of_deploy_body(
    payment: ExecutionInfo,
    session: ExecutionInfo,
    encoding=crypto.HashEncoding.HEX
    ) -> typing.Union[str, bytes, typing.List[int]]:
    """Returns a deploy body's digest.
    
    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hexademcimal string representation of a deploy body digest.

    """
    # Set data to be hashed.
    data = \
        codec.to_bytes(payment) + \
        codec.to_bytes(session)

    return crypto.get_hash(data, encoding=encoding)
