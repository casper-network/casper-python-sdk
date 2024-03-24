import dataclasses
import typing

from pycspr.types.node.sse.simple import NodeEventChannel
from pycspr.types.node.sse.simple import NodeEventType


@dataclasses.dataclass
class NodeEventInfo():
    """Encapsulates emitted event information.

    """
    # Channel over which event emitted by a node.
    channel: NodeEventChannel

    # Type of event emitted by a node.
    typeof: NodeEventType

    # Event ordinal identifier - acts as an offset.
    idx: int

    # Event payload ... typically data but sometimes a simple string.
    payload: typing.Union[dict, str]
