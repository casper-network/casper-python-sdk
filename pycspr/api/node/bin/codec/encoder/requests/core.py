from pycspr.api.node.bin.types.requests import \
    Endpoint, \
    Request
from pycspr.api.node.bin.codec.encoder.primitives import \
    encode_u8, \
    encode_u16
from pycspr.api.node.bin.codec.encoder.domain import \
    encode_protocol_version


def encode_request(entity: Request) -> bytes:
    def encode_header() -> bytes:
        def encode_endpoint() -> bytes:
            if entity.endpoint.name.startswith("Get_"):
                return encode_u8(0)
            elif entity.endpoint == Endpoint.Try_AcceptTransaction:
                return encode_u8(1)
            elif entity.endpoint == Endpoint.Try_SpeculativeExec:
                return encode_u8(2)
            else:
                raise ValueError("Invalid request type")

        return \
            encode_u16(entity.header.binary_request_version) + \
            encode_protocol_version(entity.header.chain_protocol_version) + \
            encode_endpoint() + \
            encode_u16(entity.header.id)

    def encode_payload() -> bytes:
        print("TODO: _encode_request_payload")
        return b''

    return encode_header() + encode_payload()
