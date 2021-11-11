from pycspr.serialisation import cl_u32


def from_bytes(value: bytes) -> object:
    raise NotImplementedError()
    

def to_bytes(value: object) -> bytes:
    return cl_u32.to_bytes(len(value)) + bytes([i for j in value for i in j])


def from_json(value: dict) -> object:
    raise NotImplementedError()


def to_json(value: object) -> dict:
    raise NotImplementedError()
