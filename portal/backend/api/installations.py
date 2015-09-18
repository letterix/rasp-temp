from authentication import *
from handlers import customerHandler, installationHandler, statusHandler


@accepted_roles(all_roles())
def get(customer_id):
    res = installationHandler.get_by_customer(customer_id)
    if res:
        statusHandler.set_status_for_installations(res)
    return OkResponse(res)