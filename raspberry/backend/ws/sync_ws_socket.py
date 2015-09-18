from ws4py.websocket import WebSocket
from ws.sync_users import SYNC_USERS
from sync import SyncManager
import json

class SyncWsSocket(WebSocket):

    def __init__(self, sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None):
        super(SyncWsSocket, self).__init__(sock, protocols=None, extensions=None, environ=None, heartbeat_freq=None)
        self.installation = None

    def sendData(self, data):
        self.send(data)

    def closed(self, code, reason=None):
        print("installation disconnected:", code)
        if self.installation in SYNC_USERS :
            del SYNC_USERS[self.installation]

    def received_message(self, message):
        data = message.data.decode()
        print(data)
        msg = json.loads(data)
        if msg.get('connect'):
            self.connect(msg.get('connect'))
        else:
            SyncManager.onMessage(msg)

    def connect(self, installation):
        if self.installation:
            del SYNC_USERS[installation]

        self.installation = installation
        SYNC_USERS[installation] = self
