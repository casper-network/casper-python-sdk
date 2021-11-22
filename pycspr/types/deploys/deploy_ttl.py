import dataclasses

from pycspr.utils import constants
from pycspr.utils import conversion


@dataclasses.dataclass
class DeployTimeToLive():
    """Encapsulates a timeframe within which a deploy must be processed.

    """
    # TTL in milliseconds.
    as_milliseconds: int

    # Humanized representation of the ttl.
    humanized: str

    def __eq__(self, other) -> bool:
        return self.as_milliseconds == other.as_milliseconds and \
               self.humanized == other.humanized

    @staticmethod
    def from_string(as_string: str) -> "DeployTimeToLive":
        as_milliseconds = conversion.humanized_time_interval_to_milliseconds(as_string)
        if as_milliseconds > constants.DEPLOY_TTL_MS_MAX:
            raise ValueError(f"Invalid deploy ttl. Maximum (ms)={constants.DEPLOY_TTL_MS_MAX}")

        return DeployTimeToLive(
            as_milliseconds=as_milliseconds,
            humanized=as_string
        )

    def to_string(self) -> str:
        return self.humanized
