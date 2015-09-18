# -*- coding : utf-8 -*-
from common import *
from urllib.parse import unquote
from authentication import *
from handlers import userHandler
import cherrypy, authentication
import utils.validator as validator

@accepted_roles(all_roles())
def get(username=None):
    if username:
        user = userHandler.get_user(username)
    else:
        user = get_current_user()
    if user:
        user = userHandler.safe_fields(user)
        customers = customerHandler.get_customers_for(user.get('username'))
        user['customers'] = customers
        return OkResponse(userHandler.safe_fields(user))
    else:
        return ConflictResponse("Could not fetch the user.")

@accepted_roles(all_roles())
@JsonIn
def post(input_user):
    response = userHandler.create_user(input_user)
    if response == True:
        return OkResponse(KEY_USER_CREATED)
    else:
        return ConflictResponse(response)


@accepted_roles(all_roles())
@JsonIn
def put(user):
    msg = validator.updated_user(user)
    if len(msg) == 0:
        if userHandler.update_user(user):
            msg.append(KEY_SUCCESSFUL_UPDATE)
        else:
            msg.append(KEY_NOT_MODIFIED)
        return OkResponse({'msg': msg})
    else:
        return ConflictResponse({'msg': msg})


@accepted_roles(admin_roles())
def delete(username):
    if userHandler.delete_user(username):
        return OkResponse({'removed': username})
    else:
        return ConflictResponse({'msg': KEY_COULD_NOT_REMOVE})
