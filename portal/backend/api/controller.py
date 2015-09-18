from common import *
from authentication import *
from handlers import controllerHandler, statusHandler


@accepted_roles(semi_admin_roles())
@JsonIn
def post(controller):
        res = controllerHandler.insert(controller)
        if res:
            return OkResponse(res)
        else:
            return ConflictResponse("Could not create controller")


@accepted_roles(all_roles())
def get(installation, controller_ip):
    res = controllerHandler.get_controller(installation, controller_ip)
    if res:
            statusHandler.set_status_for_controller(res)
            return OkResponse(res)
    else:
            return ConflictResponse("Could not get controller")


@accepted_roles(semi_admin_roles())
@JsonIn
def put(controller):
    res = controllerHandler.update(controller)
    if res:
        return OkResponse("Successfully updated the controller")
    else:
        return ConflictResponse("Could not update controller")


@accepted_roles(semi_admin_roles())
def delete(installation, controller_ip):
    res = controllerHandler.delete(installation, controller_ip)
    if res:
        return OkResponse("Controller was successfully deleted")
    else:
        return ConflictResponse("Could not delete controller")

