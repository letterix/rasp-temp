from common import *
from authentication import *
from handlers import statusHandler

@accepted_roles(all_roles())
def get(serial_number):
    result = statusHandler.get_status(serial_number)
    return OkResponse(result)