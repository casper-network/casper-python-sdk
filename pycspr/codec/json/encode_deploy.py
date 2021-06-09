from pycspr.types.deploy import Deploy
from pycspr.codec.json.encode_approval import encode as encode_approval
from pycspr.codec.json.encode_deploy_header import encode as encode_deploy_header
from pycspr.codec.json.encode_digest import encode as encode_digest
from pycspr.codec.json.encode_execution_info import encode as encode_execution_info



def encode(entity: Deploy):
    """Maps a domain entity to a JSON representation.

    :param entity: Domain entity being mapped.

    """
    return {
        "approvals": [encode_approval(i) for i in entity.approvals],
        "hash": encode_digest(entity.hash),
        "header": encode_deploy_header(entity.header),
        "payment": encode_execution_info(entity.payment),
        "session": encode_execution_info(entity.session)
    }
