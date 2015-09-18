from common import *
from authentication import *
from handlers import userHandler

@accepted_roles(all_roles())
def get(customer_id=None, changes=False):
    result = False
    user = userHandler.get_current_user()
    if customer_id:
        if changes:
            if allow_changes(customer_id):
                result = True
        else:
            if allow_viewing(customer_id):
                result = True
    elif user_is_master(user):
        result = True
    if result:
        return OkResponse(result)
    else:
        return ConflictResponse(result)



