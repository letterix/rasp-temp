from common import *
from authentication import *
from handlers import installationHandler, controllerHandler, statusHandler


@accepted_roles(all_roles())
def get(serial_number):
    res = controllerHandler.get_controllers(serial_number)
    if res:
        statusHandler.set_status_for_controllers(res)
        payload = {"controllers": res}
        return OkResponse(payload)
    else:
        return NotFoundResponse("Could not find any controllers for that installation and user")
