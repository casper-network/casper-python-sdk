# How To: Consume SSE Stream

## Overview


Each node exposes an [Server Side Event (SSE)](https://en.wikipedia.org/wiki/Server-sent_events) event stream, typically over port 18101.  The stream exposes a set of event channels over which realtime events are published.  To consume events a client:

- connects to the event stream by specifying:
    - sse address & port
    - channel of interest
    - a callback function
    - an event identifier for use in playback scenarios 
    
Whenever the node emits an event the consumer's callback function is invoked accordingly.  A client can optionally specify an event filter when connecting
they may specify filter  will need to specify the event channel / event type of interest 

, each event is associated with a channel.  3 channels are supported: deploys, main & sigs.

::: how_tos.how_to_consume_events
