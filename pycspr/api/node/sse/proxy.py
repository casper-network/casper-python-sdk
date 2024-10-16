import json
import typing

import requests
import sseclient

from pycspr.api.node.sse.type_defs import \
    ConnectionInfo, \
    EventInfo, \
    EventType


class Proxy:
    """Node SSE server proxy.

    """
    def __init__(self, connection_info: ConnectionInfo):
        """Instance constructor.

        :param connection_info: Information required to connect to a node.

        """
        self._connection_info = connection_info

    def yield_events(
        self,
        etype: EventType,
        eid: int = 0
    ) -> typing.Generator[EventInfo, None, None]:
        """Returns generator yielding (filterable) events emitted by a node's event stream.

        :param etype: Type of event type to listen for (all if unspecified).
        :param eid: Identifier of event from which to start stream listening.

        """
        # Set client.
        sse_client: sseclient.SSEClient = sseclient.SSEClient(
            requests.get(
                self._connection_info.get_url(eid),
                stream=True
            )
        )

        # Open connection & iterate event stream.
        try:
            for event in sse_client.events():
                try:
                    edata = json.loads(event.data)
                except json.JSONDecodeError:
                    edata = event.data

                if isinstance(edata, str):
                    etype_in = EventType.Shutdown
                else:
                    for etype_in in EventType:
                        if etype_in.name in edata:
                            break
                    else:
                        raise ValueError(f"Unknown event type: {edata}")

                if etype == EventType.All or etype == etype_in:
                    yield EventInfo(etype_in, event.id, edata)

        # On error ensure that connection is closed.
        except Exception as err:
            try:
                sse_client.close()
            except Exception as inner_err:
                print(f"Ignoring error raised on closing SSE connection: {inner_err}.")
            finally:
                raise err
