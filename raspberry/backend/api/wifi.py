from networking import Networking
from common import *
import traceback
import time

network = Networking()

def get():
    try:
        networks = network.scan_wifi_networks()
        current = network.get_current()

        data = {
            'networks' : networks,
            'current' : current
        }

        return OkResponse(data)

    except:
        traceback.print_exc()
        return ConflictResponse("KEY_ERROR")


@JsonIn
def post(params):
    print("Connect to:", params['selected'], params['password'])
    data = {}
    try:
        network.select_wifi_network(params['selected'], params['password'])

        for i in range(10):
            data['current'] = network.get_current()
            if data['current']['ip']:
                break
            else:
                time.sleep(i)
        else:
            return ErrorResponse("KEY_WIFI_CONNECT_ERROR")


    except:
        return ErrorResponse("KEY_WIFI_CONNECT_ERROR")
    return OkResponse(data)
