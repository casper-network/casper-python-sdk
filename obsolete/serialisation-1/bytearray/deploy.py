from pycspr.serialisation.bytearray import deploy_approval
from pycspr.serialisation.bytearray import deploy_header
from pycspr.serialisation.bytearray import deploy_executable_item
from pycspr.types import Deploy


def from_bytes(value: bytes) -> Deploy:
    raise NotImplementedError()


def from_json(obj: dict) -> Deploy:
    return Deploy(
        approvals=[deploy_approval.from_json(i) for i in obj["approvals"]],
        hash=bytes.fromhex(obj["hash"]),
        header=deploy_header.from_json(obj["header"]),
        payment=deploy_executable_item.from_json(obj["payment"]),
        session=deploy_executable_item.from_json(obj["session"])
    )


def to_bytes(entity: Deploy) -> bytes:
    raise NotImplementedError()


def to_json(entity: Deploy) -> dict:
    return {
        "approvals": [deploy_approval.to_json(i) for i in entity.approvals],
        "hash": entity.hash.hex(),
        "header": deploy_header.to_json(entity.header),
        "payment": deploy_executable_item.to_json(entity.payment),
        "session": deploy_executable_item.to_json(entity.session)
    }
