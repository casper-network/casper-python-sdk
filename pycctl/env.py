import enum
import os


class EVarType(enum.Enum):
    CCTL = "CCTL"


def get_evar(evar: EVarType) -> object:
    return os.getenv(evar.name)
