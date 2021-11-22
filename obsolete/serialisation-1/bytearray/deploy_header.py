from pycspr.types import DeployHeader
from pycspr.serialisation.bytearray import cl_public_key
from pycspr.serialisation.bytearray import deploy_timestamp
from pycspr.serialisation.bytearray import deploy_ttl


def from_bytes(value: bytes) -> DeployHeader:
    raise NotImplementedError()
    

def from_json(entity: dict) -> DeployHeader:
    return DeployHeader(
        account_public_key=cl_public_key.from_json(obj["account"]),
        body_hash=bytes.fromhex(obj["body_hash"]),
        chain_name=obj["chain_name"],
        dependencies=[],
        gas_price=obj["gas_price"],
        timestamp=deploy_timestamp.from_json(obj["timestamp"]),
        ttl=deploy_ttl.from_json(obj["ttl"])
    )


def to_bytes(entity: DeployHeader) -> bytes:
    raise NotImplementedError()


def to_json(entity: DeployHeader) -> dict:
    return {
        "account": cl_public_key.to_json(entity.account_public_key),
        "body_hash": entity.body_hash.hex(),
        "chain_name": entity.chain_name,
        "dependencies": entity.dependencies,
        "gas_price": entity.gas_price,
        "timestamp": deploy_timestamp.to_json(entity.timestamp),
        "ttl": deploy_ttl.to_json(entity.ttl)
    }
