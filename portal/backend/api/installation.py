from common import *
from authentication import *
from handlers import installationHandler, controllerHandler, statusHandler

@accepted_roles(semi_admin_roles())
@JsonIn
def post(installation):
        res = installationHandler.create(installation['serial_number'], 'pi', installation['name'], installation['customer'])
        if res:
            return OkResponse("Successfully added a new installation")
        else:
            return ConflictResponse("Could not add the installation")

@accepted_roles(all_roles())
def get(installation):
    res = installationHandler.get(installation)
    if res:
        statusHandler.set_status_for_installation(res)
        return OkResponse(res)
    else:
        return ConflictResponse("Could not get the installation")

@JsonIn
@accepted_roles(semi_admin_roles())
def put(installation):
    res = installationHandler.update_installation(installation)
    if res:
        return OkResponse("Successfully updated the installation")
    else:
        return ConflictResponse("Could not update the installation with that serial/user/customer")


@accepted_roles(semi_admin_roles())
def delete(serial_number):
    res = installationHandler.delete_installation(serial_number)
    if res:
        return OkResponse("Successfully remove the installation")
    else:
        return ConflictResponse("Could not delete the installation with that serial/user/customer")