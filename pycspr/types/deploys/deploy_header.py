import dataclasses
import typing

from pycspr.types.other.keys import PublicKey
from pycspr.types.other.timestamp import Timestamp
from pycspr.types.deploys.deploy_ttl import DeployTimeToLive


@dataclasses.dataclass
class DeployHeader():
    """Encapsulates header information associated with a deploy.

    """
    # Public key of account dispatching deploy to a node.
    account_public_key: PublicKey

    # Hash of deploy payload.
    body_hash: bytes

    # Name of target chain to which deploy will be dispatched.
    chain_name: str

    # Set of deploys that must be executed prior to this one.
    dependencies: typing.List[bytes]

    # Multiplier in motes used to calculate final gas price.
    gas_price: int

    # Timestamp at point of deploy creation.
    timestamp: Timestamp

    # Time interval after which the deploy will no longer be considered for processing by a node.
    ttl: DeployTimeToLive

    def __eq__(self, other) -> bool:
        return self.account_public_key == other.account_public_key and \
               self.body_hash == other.body_hash and \
               self.chain_name == other.chain_name and \
               self.dependencies == other.dependencies and \
               self.gas_price == other.gas_price and \
               self.timestamp == other.timestamp and \
               self.ttl == other.ttl
