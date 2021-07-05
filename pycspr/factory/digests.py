
from pycspr import factory
from pycspr import codec
from pycspr import crypto
from pycspr.types.cl import CLTypeKey
from pycspr.types.deploy import ExecutionInfo
from pycspr.types.deploy import DeployHeader



def get_digest_of_deploy(header: DeployHeader) -> str:
    """Returns a deploy's digest.
    
    :param header: Deploy header information.
    :returns: Hexademcimal string representation of a deploy digest.

    """
    # Element 1: account. 
    cl_account = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.PUBLIC_KEY),
        header.account
    )

    # Element 2: timestamp. 
    cl_timestamp = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.U64),
        header.timestamp
    )

    # Element 3: ttl. 
    cl_ttl = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.U64),
        header.timestamp
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
        factory.cl.create_simple(CLTypeKey.STRING),
        header.chain_name
    )

    # Element 7: chain-name. 
    cl_chain_name = factory.cl.create_value(
        factory.cl.create_simple(CLTypeKey.STRING),
        header.chain_name
    )

    print(cl_timestamp)

    # Set data to be hashed.
    data = \
        codec.encode(cl_account, 'byte-array') + \
        codec.encode(cl_timestamp, 'byte-array') + \
        codec.encode(cl_ttl, 'byte-array') + \
        codec.encode(cl_gas_price, 'byte-array') + \
        codec.encode(cl_body_hash, 'byte-array') + \
        codec.encode(cl_dependencies, 'byte-array') + \
        codec.encode(cl_chain_name, 'byte-array')
    
    return crypto.get_hash(data, encoding=crypto.HashEncoding.HEX)


def get_digest_of_deploy_body(payment: ExecutionInfo, session: ExecutionInfo) -> str:
    """Returns a deploy body's digest.
    
    :param payment: Deploy payment execution logic.
    :param session: Deploy session execution logic.
    :returns: Hexademcimal string representation of a deploy body digest.

    """
    # Set data to be hashed.
    data = \
        codec.encode(payment, 'byte-array') + \
        codec.encode(session, 'byte-array')

    return crypto.get_hash(data, encoding=crypto.HashEncoding.HEX)
