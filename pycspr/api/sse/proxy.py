import dataclasses
import json
import typing

import requests
import sseclient

from pycspr.api import constants
from pycspr.api.sse.types import NodeEventChannel
from pycspr.api.sse.types import NodeEventInfo
from pycspr.api.sse.types import NodeEventType


@dataclasses.dataclass
class Proxy:
    """Node SSE server proxy.

    """
    # Host address.
    host: str = constants.DEFAULT_HOST

    # Number of exposed SSE port.
    port: int = constants.DEFAULT_PORT_SSE

    @property
    def address(self) -> str:
        """A node's SSE server base address."""
        return f"http://{self.host}:{self.port}/events"

    def __str__(self):
        """Instance string representation."""
        return self.address

    def yield_events(
        self,
        echannel: NodeEventChannel,
        etype: NodeEventType = None,
        eid: int = 0
    ) -> typing.Generator[NodeEventInfo, None, None]:
        """Returns a generator that will yield (filterable) events emitted by a node's event stream.

        :param echannel: Type of event channel to which to bind.
        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        # Open client connection.
        sse_client = self._get_client(echannel, eid)
        try:
             # Iterate event stream.
            for event in sse_client.events():
                # Set event payload.
                try:
                    payload = json.loads(event.data)
                except json.JSONDecodeError:
                    payload = event.data

                # Set event type.
                if isinstance(payload, str):
                    typeof = NodeEventType.Shutdown
                else:
                    for typeof in NodeEventType:
                        if typeof.name in payload:
                            break
                    else:
                        raise ValueError(f"Unknown event type: {payload}")

                # If event type is in scope then yield event information.
                if etype is None or etype == typeof:
                    yield NodeEventInfo(echannel, etype, event.id, payload)

        # On error ensure that client connection is closed.
        except Exception as err:
            try:
                sse_client.close()
            except Exception as inner_err:
                print(f"Ignoring error raised on closing SSE connection: {inner_err}.")
            finally:
                raise err

    def _get_client(self, echannel: NodeEventChannel, eid: int = 0) -> sseclient.SSEClient:
        """Returns an SSE client instant targeting appropriate event channel.
        
        :param echannel: Type of event channel to which to bind.
        :param eid: Identifier of event from which to start stream listening.
        :returns: Configured event channel instance.

        """
        url = f"{self.address}/{echannel.name.lower()}"
        if eid:
            url = f"{url}?start_from={eid}"

        return sseclient.SSEClient(requests.get(url, stream=True))
