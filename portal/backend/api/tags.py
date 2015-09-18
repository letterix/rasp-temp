from common import *
from authentication import *
from handlers import controllerHandler, tagHandler, logHandler, statusHandler
from ws import sync_ws_socket


@accepted_roles(all_roles())
def get(installation, controller_ip):
    tag_list = tagHandler.get_tags(installation, controller_ip)
    if tag_list:
        tag_list = statusHandler.set_status_for_tags(tag_list)
    payload = {'tags': tag_list}
    return OkResponse(payload) if len(tag_list) > 0 else ConflictResponse(payload)