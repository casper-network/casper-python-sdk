from typing import Union


def get_block_id_param(block_id: Union[str, int] = None) -> dict:
    """ converts block id into rpc param depending on the type of block id. """

    if block_id is None:
        return {}
    elif isinstance(block_id, str):
        return {"block_identifier": {"Hash": block_id}}
    elif isinstance(block_id, int):
        return {"block_identifier": {"Height": block_id}}
    else:
        raise TypeError(f"block_id should be str or int not "
                        f"{type(block_id)}! (block_id: {block_id})")
