from handlers import settingsHandler, userHandler, syncHandler, logHandler
from config import RUN_SYNC_FREQUENCY
from ws.sync_users import SYNC_INSTALLATIONS
import json
from sync.sync_methods import *
import config
import traceback

def run():
    try:
        sync_entries = syncHandler.get_all()
        print("Syncing %s entries." % (len(sync_entries)))
        for sync in sync_entries:
            sendMessage(sync['installation'], sync)
    except:
        traceback.print_exc()


def onMessage(msg):
    #print("onMessage: " + json.dumps(msg))

    if msg.get("ping"):
        return

    if msg.get('ack'):
        if msg.get('correction'):
            handle_correction_ack(msg)
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
        if installation in SYNC_INSTALLATIONS:
            syncHandler.set_attempt_time(sync)
            del sync['last_sync_attempt']
            #print("sendMessage: " + json.dumps(sync))
            SYNC_INSTALLATIONS[installation].sendData(json.dumps(sync))
    except Exception as e:
        handle_send_error(installation, e)

def send_ping(installation):
    try:
        if installation in SYNC_INSTALLATIONS:
            SYNC_INSTALLATIONS[installation].sendData('{"ping": "pong"}')
    except Exception as e:
        return False
    return True

def handle_send_error(installation, error):
    print("ERROR: sendMessage:" + str(error))
    traceback.print_exc()

def sendAck(id, installation):
    ack =  {"ack":id, 'installation': installation}
    #print("ACK_MSG: " + str(ack))
    try:
        if installation in SYNC_INSTALLATIONS:
            SYNC_INSTALLATIONS[installation].sendData(json.dumps(ack))
    except Exception as e:
        print("ERROR: ackMessage:" + str(e))

def send_correction_ack(id, installation, data):
    ack =  {"ack":id, 'installation': installation, 'correction': json.dumps(data)}
    #print("ACK_MSG: " + str(ack))
    try:
        if installation in SYNC_INSTALLATIONS:
            SYNC_INSTALLATIONS[installation].sendData(json.dumps(ack))
    except Exception as e:
        print("ERROR: ackMessage:" + str(e))

def handleAck(msg):
    acked = syncHandler.delete(msg.get('ack'), msg.get('installation'))
    #print("ACKED:", acked, msg['installation'])

def handle_correction_ack(msg):
    sync_entry = syncHandler.get(msg['ack'])
    table = sync_entry['table']
    #if table == 'users':
        #userHandler.update_user(json.loads(msg['correction']), False)
    #elif table == 'settings':
        #settingsHandler.update_setting(json.loads(msg['correction']), msg['installation'], False)


def handleInsert(msg):
    table, data, installation = msg['table'], json.loads(msg['data']), msg['installation']

    if table == 'log':
        return logHandler.create_log_entry(data, installation)
    else:
        print("ERROR: Unsupported table: %s" % (table))

    return True

def handleUpdate(msg):
    table = msg['table']
    data = json.loads(msg['data'])
    installation = msg['installation']

    if table == 'settings':
        if config.LOCAL:
            current_setting = settingsHandler.get_setting(installation, data['setting_name'])
            prev = json.loads(msg['prev'])
            if prev != current_setting:
                send_correction_ack(msg['id'], installation, current_setting)
                return False
            else:
                settingsHandler.update_setting(data, installation, False)
        else:
            settingsHandler.update_setting(data, installation, False)
    else:
        print("ERROR: Unsupported table: %s" % (table))

    return True

def handleDelete(msg):
    table, data, installation = msg['table'], json.loads(msg['data']), msg['installation']

    if table == 'users':
        userHandler.delete_user(data['username'], False)
    else:
        print("Error: Unsupported table: %s" % (table))

    return True

def register(installation, ws):
    SYNC_INSTALLATIONS[installation] = ws

def un_register(installation):
    SYNC_INSTALLATIONS[installation].close()
    del SYNC_INSTALLATIONS[installation]
