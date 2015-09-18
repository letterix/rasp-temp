from common import *
from authentication import *
import authentication
from dao import sync_queue_dao

@accepted_roles(all_roles())
def get():
    user = authentication.get_current_user()
    syncs = sync_queue_dao.get_by_burner_sn(user.get('burner_sn'))
    return OkResponse(syncs)

@accepted_roles(all_roles())
def post():
    user = authentication.get_current_user()
    sync_queue_dao.handle_syncs(user)
