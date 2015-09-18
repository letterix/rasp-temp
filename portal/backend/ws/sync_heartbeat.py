from sync import SyncManager
from config import LOCAL
from ws.sync_users import SYNC_INSTALLATIONS
import traceback

def send_ping():
    try:
        print('Central sending pings')
        failed = []
        for key in SYNC_INSTALLATIONS:
            print('pinging ', key)
            ok = SyncManager.send_ping(key)
            if not ok:
                failed.append(key)
        for fail in failed:
            SyncManager.un_register(fail)
    except:
        traceback.print_exc()
        pass
