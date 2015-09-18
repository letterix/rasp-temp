from common import *
from handlers import userHandler
import cherrypy

def get():
    user = userHandler.get_user()
    user['password'] = ""
    user['salt'] = ""
    return OkResponse(user)


