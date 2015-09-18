from common import *
from authentication import *
from handlers import controllerHandler, tagHandler, logHandler, statusHandler, installationHandler, customerHandler, mailHandler
from ws import sync_ws_socket


@accepted_roles(all_roles())
def get():
    tag = {"name":"WARNING_SECOND", "value": 1, "controller_ip": "192.168.0.1", "time": "2014-10-20T11:32:33.744353"}
    installation = "66002174487292"
    installation_obj = installationHandler.get(installation, True)
    controller_obj = controllerHandler.get_controller(installation, tag['controller_ip'], True)
    customer_obj = customerHandler.get_customer(installation_obj['customer'])
    res = mailHandler.send_alarm_mail(tag, installation_obj, controller_obj, customer_obj)
    return OkResponse('Sent the mail!')