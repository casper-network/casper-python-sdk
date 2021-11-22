import json
import typing

from pycspr.serialisation.bytearray import cl_value
from pycspr.serialisation.bytearray import cl_value_parsed
from pycspr.serialisation.bytearray import deploy
from pycspr.serialisation.bytearray import deploy_argument
from pycspr.serialisation.bytearray import deploy_executable_item
from pycspr.serialisation.bytearray import deploy_header
from pycspr.types import CLValue
from pycspr.types import Deploy
from pycspr.types import DeployHeader
from pycspr.types import DeployArgument
from pycspr.types import DeployExecutableItem


# Map: Domain entity type <-> serialiser.
_SERIALISERS = {
    Deploy: deploy,
    DeployArgument: deploy_argument,
    DeployExecutableItem: deploy_executable_item,
    DeployHeader: deploy_header
}


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()


def from_json(value: str) -> object:
    obj = json.loads(value)

    return deploy.from_json(obj)


def to_bytes(entity: object) -> bytes:
    if type(entity) == CLValue:
        return cl_value_parsed.to_bytes(entity)
    elif type(entity) in _SERIALISERS:
        return _SERIALISERS[type(entity)].to_bytes(entity)
    elif issubclass(type(entity), DeployExecutableItem):
        return deploy_executable_item.to_bytes(entity)
    else:
        raise ValueError("Domain entity cannot be mapped to bytes")


def to_json(entity: object) -> str:
    if type(entity) == CLValue:
        obj = cl_value_parsed.to_json(entity)
    elif type(entity) in _SERIALISERS:
        obj = _SERIALISERS[type(entity)].to_json(entity)
    elif issubclass(type(entity), DeployExecutableItem):
        obj = deploy_executable_item.to_json(entity)
    else:
        raise ValueError("Domain entity cannot be mapped to JSON")

    return json.dumps(obj)
