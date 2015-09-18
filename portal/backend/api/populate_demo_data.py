from common import *
from authentication import *
import authentication
from sync import sync_methods
from handlers import tagHandler, syncHandler

@accepted_roles(admin_roles())
def get():
    tags = [
        {"name": "YEAR", "address": "%MW0", "type": "value", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "MONTH", "address": "%MW1", "type": "value", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "DAY", "address": "%MW2", "type": "value", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "HOUR", "address": "%MW3", "type": "value", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "MINUTE", "address": "%MW4", "type": "value", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "SECOND", "address": "%MW5", "type": "value", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "ALARM_MINUTE", "address": "%MW4:X0", "type": "alarm", "controller_ip": "192.168.0.1", "installation":"66002174487292"},
        {"name": "WARNING_SECOND", "address": "%MW5:X1", "type": "warning", "controller_ip": "192.168.0.1", "installation":"66002174487292"}
    ]
    res = []
    for tag in tags:
        res.append(tagHandler.insert(tag))
    for i in range(0,255):
        addr_num = i % 12
        name = "gen_tag_%s"%(i,)
        address = "%%MW%s" % (addr_num,)
        type = "value"
        controller_ip = "192.168.0.1"
        installation = "66002174487292"
        gen_tag = {"name": name, "address": address, "type": type, "controller_ip": controller_ip, "installation": installation}
        res.append(tagHandler.insert(gen_tag))
    if not (False in res or None in res):
        return OkResponse("Successfully added the new tag")
    else:
        return ConflictResponse("Could not insert the tag for that controller/installation/customer")

