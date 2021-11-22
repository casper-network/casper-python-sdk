from pycspr.types import DeployTimeToLive
from pycspr.utils import constants
from pycspr.utils import conversion


def from_bytes(value: bytes) -> DeployTimeToLive:
    raise NotImplementedError()


def to_bytes(entity: DeployTimeToLive) -> bytes:
    raise NotImplementedError()


def from_json(value_humanized: str) -> DeployTimeToLive:
    as_milliseconds = conversion.humanized_time_interval_to_milliseconds(value_humanized)
    if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
        raise ValueError(f"Invalid deploy ttl.  Maximum (ms) = {constants.DEPLOY_TTL_MS_MAX}")

    return DeployTimeToLive(
        as_milliseconds=as_milliseconds,
        humanized=value_humanized
    )


def to_json(entity: DeployTimeToLive) -> dict:
    return entity.humanized
