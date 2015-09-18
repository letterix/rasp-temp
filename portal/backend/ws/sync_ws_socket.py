from ws4py.websocket import WebSocket
from ws.sync_users import SYNC_INSTALLATIONS
from sync import SyncManager
from handlers import installationHandler
import json

class SyncWsSocket(WebSocket):

    def __init__(self, sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None):
        super(SyncWsSocket, self).__init__(sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None)
        self.installation = None

    def sendData(self, data):
        self.send(data)

    def closed(self, code, reason=None):
        print("installation disconnected:", code)
        if self.installation in SYNC_INSTALLATIONS :
            del SYNC_INSTALLATIONS[self.installation]

    def received_message(self, message):
        data = message.data.decode()
        #print(data)
        msg = json.loads(data)
        if msg.get('connect'):
            self.connect(msg.get('installation'), msg.get('model'))
        else:
            SyncManager.onMessage(msg)

    def connect(self, installation, model):

        if not installationHandler.is_registered(installation):
            installationHandler.register(installation, model, "")

        if self.installation:
            del SYNC_INSTALLATIONS[installation]

        self.installation = installation
        SYNC_INSTALLATIONS[installation] = self

