from common import *
from authentication import *
from handlers import userHandler
import cherrypy, authentication
import utils.validator as validator

@accepted_roles(all_roles())
def get():
    users = userHandler.get_users()
    result = []
    if users:
        for user in users:
            user = userHandler.safe_fields(user)
            customers = customerHandler.get_customers_for(user.get('username'))
            user['customers'] = customers
            result.append(userHandler.safe_fields(user))
        return OkResponse(result)
    else:
        return ConflictResponse("No users could be fetched with the current user")