from sync import SyncManager
from handlers import installationHandler
from config import LOCAL
from ws.sync_users import SYNC_USERS
import traceback

def send_ping():
    try:
        if LOCAL:
            print('Local sending ping')
            SyncManager.send_ping(installationHandler.get_installation()['serial_number'])
        else:
            print('Central sending pings')
            failed = []
            for key in SYNC_USERS:
                print('pinging ', key)
                ok = SyncManager.send_ping(key)
                if not ok:
                    failed.append(key)
            for fail in failed:
                SyncManager.un_register(fail)
    except:
        traceback.print_exc()
        pass
