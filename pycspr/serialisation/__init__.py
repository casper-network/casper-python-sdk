import json
import typing

from pycspr.serialisation import cl_type
from pycspr.serialisation import cl_value
from pycspr.serialisation import cl_value_parsed
from pycspr.serialisation import deploy
from pycspr.serialisation import deploy_approval
from pycspr.serialisation import deploy_argument
from pycspr.serialisation import deploy_executable_item
from pycspr.serialisation import deploy_header
from pycspr.serialisation import deploy_ttl
from pycspr.serialisation.cl_value_parsed import CL_VALUE_SERIALISERS
from pycspr.types import CLType
from pycspr.types import CLValue
from pycspr.types import Deploy
from pycspr.types import DeployApproval
from pycspr.types import DeployArgument
from pycspr.types import DeployHeader
from pycspr.types import DeployTimeToLive
from pycspr.types import DeployExecutableItem



# Map: Domain entity type <-> serialiser.
_SERIALISERS = {
    CLType: cl_type,
    CLValue: cl_value,
    Deploy: deploy,
    DeployApproval: deploy_approval,
    DeployArgument: deploy_argument,
    DeployExecutableItem: deploy_executable_item,
    DeployHeader: deploy_header,
    DeployTimeToLive: deploy_ttl,
}


def from_bytes(entity_as_bytes: bytes) -> object:
    """Mapper: byte array -> domain entity.

    :param entity_as_bytes: A domain entity serialised as a byte array.
    :returns: Deserialised domain entity.

    """
    raise NotImplementedError()


def to_bytes(entity: object) -> bytes:
    """Mapper: domain entity -> byte array.

    :param entity: A domain entity.
    :returns: A domain entity serialised as a bytes array.

    """
    serialiser = _get_serialiser(type(entity))

    return serialiser.to_bytes(entity)


def from_json(entity_type: typing.Type, entity_as_json: str) -> object:
    """Mapper: JSON text blob -> domain entity.

    :param entity_as_json: A domain entity serialised as a JSON text blob.
    :param entity_type: Type of domain entity to be deserialised.
    :returns: Deserialised domain entity.

    """
    print(entity_type, entity_as_json)
    serialiser = _get_serialiser(entity_type)

    return serialiser.from_json(json.loads(entity_as_json))


def to_json(entity: object) -> str:
    """Mapper: domain entity -> JSON text blob.

    :param entity: A domain entity.
    :returns: A domain entity serialised as a JSON text blob.

    """
    serialiser = _get_serialiser(type(entity))

    return json.dumps(serialiser.to_json(entity))


def _get_serialiser(entity_type: typing.Type) -> typing.Callable:
    """Returns a serialiser by entity type (or it's parent type).

    """
    if entity_type in _SERIALISERS:
        return _SERIALISERS[entity_type]
    elif entity_type.__bases__ and entity_type.__bases__[0] in _SERIALISERS:
        return _SERIALISERS[entity_type.__bases__[0]]
    else:
        raise ValueError("Domain entity cannot be mapped to a serialiser")    
