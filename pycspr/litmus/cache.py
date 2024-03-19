import json
import os
import pathlib
import sys
import typing

_PATH_TO_BLOCKS = pathlib.Path("/Users/asladeofgreen/Work/cspr/l1/litmus/tests/assets/blocks")

_STORE_BY_HASH: dict = dict()
_STORE_BY_HEIGHT: dict = dict()

from pycspr.litmus import decoder
from pycspr.litmus.types import Block


def init():
    for _, _, fnames in os.walk(_PATH_TO_BLOCKS):
        break

    for fname in fnames:
        with open(_PATH_TO_BLOCKS / fname, "r") as fstream:            
            block: Block = decoder.decode(Block, json.loads(fstream.read()))
        _STORE_BY_HASH[block.hash] = block
        _STORE_BY_HEIGHT[block.header.height] = block


def get_block_by_hash(block_id: bytes) -> typing.Optional[Block]:
    try:
        return _STORE_BY_HASH[block_id]
    except KeyError:
        pass


def get_block_by_height(block_id: int) -> typing.Optional[Block]:
    try:
        return _STORE_BY_HEIGHT[block_id]
    except KeyError:
        pass
