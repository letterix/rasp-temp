from authentication import *
from handlers import customerHandler, statusHandler

@accepted_roles(all_roles())
def get():
    customers = customerHandler.get_customers()
    if customers:
        res = [c for c in customers if allow_viewing(c['id']) and c.get('name') != 'master']
        statusHandler.set_status_for_customers(res)
        payload = {"customers": res}
        return OkResponse(payload)
    else:
        return NotFoundResponse("Could not find any customers")

