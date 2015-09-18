from handlers import syncHandler
from ws.sync_users import SYNC_USERS, LAST_RECIVED_PING
import json
from sync.sync_methods import *
import config,logging
import traceback
import datetime
from handlers import modbus_connector,tagHandler
from config import LOCAL

LOG = logging.getLogger()


def run():
    try:
        sync_entries = syncHandler.get_all()
        #print("Syncing %s entries." % (len(sync_entries)))
        for sync in sync_entries:
            sendMessage(sync['installation'], sync)
    except:
        traceback.print_exc()


def onMessage(msg):
    #print("onMessage: " + json.dumps(msg))

    if msg.get("ping"):
        if LOCAL:
            LAST_RECIVED_PING['ping'] = datetime.datetime.now()
        return

    if msg.get('ack'):
        handleAck(msg)
    else:
        method, table = msg.get('method'), msg.get('table')

        if method == INSERT:
            ok = handleInsert(msg)
        elif method == UPDATE:
            ok = handleUpdate(msg)
        elif method == DELETE:
            ok = handleDelete(msg)
        else:
            print("ERROR: Method not supported: %s" % (method))
        if ok:
            sendAck(msg['id'], msg['installation'])


def sendMessage(installation, sync):
    try:
        if installation in SYNC_USERS:
            syncHandler.set_attempt_time(sync)
            del sync['last_sync_attempt']
            #print("sendMessage: " + json.dumps(sync))
            SYNC_USERS[installation].sendData(json.dumps(sync))
    except Exception as e:
        handle_send_error(installation, e)


def send_ping(installation):
    try:
        if installation in SYNC_USERS:
            SYNC_USERS[installation].sendData('{"ping": "pong"}')
    except Exception as e:
        return False
    return True


def handle_send_error(installation, error):
    print("ERROR: sendMessage:" + str(error))
    traceback.print_exc()


def sendAck(id, installation):
    ack = {"ack":id, 'installation': installation}
    #print("ACK_MSG: " + str(ack))
    try:
        if installation in SYNC_USERS:
            SYNC_USERS[installation].sendData(json.dumps(ack))
    except Exception as e:
        print("ERROR: ackMessage:" + str(e))


def handleAck(msg):
    acked = syncHandler.delete(msg.get('ack'), msg.get('installation'))
    #print("ACKED:", acked, msg['installation'])


def handleInsert(msg):

    table, data, installation = msg['table'], json.loads(msg['data']), msg['installation']
    if table == 'tags':
        if not tagHandler.insert(data):
            LOG.error("Failed to insert a new tag!")
    else:
        print("ERROR: Unsupported table: %s" % (table))

    return True


def handleUpdate(msg):
    table = msg['table']
    data = json.loads(msg['data'])
    installation = msg['installation']

    if table == 'tags':
        if data['name']:
            return tagHandler.update(data)

        print("ERROR: Could not update table: %s" % (table))
    else:
        print("ERROR: Unsupported table: %s" % (table))

    return False


def handleDelete(msg):
    table, data, installation = msg['table'], json.loads(msg['data']), msg['installation']
    if table == 'tags':
        if data['name']:
            return tagHandler.delete(data['name'], data['controller_ip'])
    else:
        print("Error: Unsupported table: %s" % (table))

    return False


def register(installation, ws):
    SYNC_USERS[installation] = ws


def un_register(installation):
    SYNC_USERS[installation].close()
    del SYNC_USERS[installation]


def clear_socket(installation):
    SYNC_USERS[installation].clear_client_var()
