from pycspr.serialisation import cl_public_key
from pycspr.types import DeployApproval


def from_bytes(value: bytes) -> DeployApproval:
    raise NotImplementedError()
    

def to_bytes(entity: DeployApproval) -> bytes:
    raise NotImplementedError()


def from_json(obj: dict) -> DeployApproval:
    return DeployApproval(
        signer=cl_public_key.from_json(obj["signer"]),
        signature=bytes.fromhex(obj["signature"]),
    )

def to_json(entity: DeployApproval) -> dict:
    return {
        "signature": entity.signature.hex(),
        "signer": entity.signer.hex()
    }
