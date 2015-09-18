__author__ = 'rasmusletterkrantz'
from common import *
from authentication import *
import authentication
from sync import sync_methods
from datetime import datetime
from handlers import tagHandler, syncHandler, installationHandler, customerHandler, controllerHandler, logHandler

@accepted_roles(admin_roles())
def get():
    d2 = datetime.now()
    res = []
    for i in range(4, 9):
        name = "customer-%d" % (i,)
        customer = {"name":name}
        res.append(customerHandler.insert(customer))
        for j in range(0, 5):
            installation_name = "installation-%d" % (j,)
            serial_number = "%s66002174487%d" % (customer.get('name'),j)
            installation = {"name":installation_name, "serial_number":serial_number, "customer": i}
            res.append(installationHandler.register(serial_number, "", ""))
            installationHandler.update_installation(installation)
            for k in range(0, 5):
                ip = "192.168.0.0.%d" % (k,)
                controller_name = "controller-%d" % (k,)
                controller = {"ip":ip, "installation": serial_number, "name":controller_name}
                res.append(controllerHandler.insert(controller))
                for l in range(0, 100):
                    address = "%%MW%d" % (l,)
                    tag_name = "LOAD_%d"% (l,)
                    tag = {"controller_ip":ip, "installation":serial_number, "type":"value", "address": address, "name": tag_name}
                    res.append(tagHandler.insert(tag, True))
                    tag['time'] = d2
                    tag['value'] = str(l)
                    res.append(logHandler.create_log_entry(tag, serial_number))
    if not (False in res or None in res):
        return OkResponse("Successfully added the data")
    else:
        return ConflictResponse("Could not insert the data..")

