import traceback
from ws4py.client.threadedclient import WebSocketClient
import config
import json, datetime
from sync import SyncManager
from handlers import installationHandler
from ws.sync_users import LAST_RECIVED_PING

WS_CLIENT = None

def check_sync_ws():
    try:
        if config.LOCAL:

            #print('checking sync ws')
            global WS_CLIENT
            if WS_CLIENT is None:
                print('init sync ws')
                WS_CLIENT = SyncWsClient(config.SYNC['url'], protocols=['http-only', 'chat'])
                WS_CLIENT.start()
            else:
                threshold_date = datetime.datetime.now() - datetime.timedelta(minutes=15)
                #print("Last sync: ", LAST_RECIVED_PING['ping'])
                #print("Threshold date: ", threshold_date)
                if LAST_RECIVED_PING['ping'] < threshold_date:
                    print('No ping received in 15 minutes, un-registering and clearing socket')
                    WS_CLIENT.clear_client_var()
                    LAST_RECIVED_PING['ping'] = datetime.datetime.now()


    except:
        traceback.print_exc()

class SyncWsClient(WebSocketClient):


    def opened(self):
        print('sync ws opened')
        current_installation = installationHandler.get_installation()
        SyncManager.register(current_installation['serial_number'], self)
        connect = {'connect': True, "installation": current_installation['serial_number'], "model": current_installation['model']}
        self.sendData(json.dumps(connect))

    def closed(self, code, reason=None):
        self.clear_client_var()

    def close_connection(self):
        self.clear_client_var()

    def received_message(self, m):
        data = m.data.decode()
        SyncManager.onMessage(json.loads(data))

    def sendData(self, data):
        self.send(data)

    def start(self):
        print('starting sync ws')
        try:
            self.connect()
        except:
            traceback.print_exc()
            self.clear_client_var()
        #self.run_forever()

    def clear_client_var(self):
        print("clearing sync var")
        global WS_CLIENT
        WS_CLIENT = None;