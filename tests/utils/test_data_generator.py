import random

from mimesis import Field, Fieldset, Schema
from mimesis.enums import Gender, TimestampFormat
from mimesis.locales import Locale


_field = Field(Locale.EN, seed=0xff)
_fieldset = Fieldset(Locale.EN, seed=0xff)


def get_chain_name():
    return _field("text.word")


def get_digest():
    return random.randbytes(32)


def get_timestamp_posix() -> int:
    return _field("timestamp", fmt=TimestampFormat.POSIX)
