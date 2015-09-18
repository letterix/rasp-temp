from common import *
from authentication import *
import authentication
from sync import sync_methods
from handlers import tagHandler, syncHandler


@accepted_roles(all_roles())
def get(installation, controller_ip, tag_name):
    tag = tagHandler.get_tag_by_name(installation, controller_ip, tag_name)
    if tag:
        return OkResponse(tag) if tag else ConflictResponse("Could not get the tag!")


@accepted_roles(semi_admin_roles())
@JsonIn
def post(tag):
    res = tagHandler.insert(tag)
    if res:
        return OkResponse("Successfully added the new tag")
    else:
        return ConflictResponse("Could not insert the tag for that controller/installation/customer")


@accepted_roles(semi_admin_roles())
@JsonIn
def put(tag):
    res = tagHandler.update(tag)
    if res:
        return OkResponse("Successfully updated the given tag")
    else:
        return ConflictResponse("Could not update the tag for that controller/installation/customer")


@accepted_roles(semi_admin_roles())
def delete(installation, controller_ip, tag_name=None):
    if tag_name is None:
        res = tagHandler.delete_by_controller(installation, controller_ip)
    else:
        res = tagHandler.delete(installation, controller_ip, tag_name)
    if res:
        return OkResponse("Successfully removed the tag")
    else:
        return ConflictResponse("Could not delete the tag for that controller/installation/customer")
