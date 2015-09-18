from common import *
from authentication import *
import time
from handlers import logHandler

@accepted_roles(all_roles())
def get(serial_number, fromDate, toDate):
    format = '%Y-%m-%d'
    fromDate = time.strptime(fromDate, format)
    toDate = time.strptime(toDate, format)
    log = logHandler.get_log_items_for(serial_number, fromDate, toDate)
    return OkResponse(log)
