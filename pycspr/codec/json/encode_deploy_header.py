from pycspr.types.deploy import DeployHeader
from pycspr.codec.json.encode_digest import encode as encode_digest
from pycspr.codec.json.encode_timestamp import encode as encode_timestamp



def encode(entity: DeployHeader):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "account": entity.account,
        "body_hash": encode_digest(entity.body_hash),
        "chain_name": entity.chain_name,
        "dependencies": entity.dependencies,
        "gas_price": entity.gas_price,
        "timestamp": encode_timestamp(entity.timestamp),
        "ttl": entity.ttl
    }
