from common import *
from authentication import *
import authentication
from handlers import settingsHandler

@accepted_roles(all_roles())
def get(setting_name = None):
    user = authentication.get_current_user()
    if setting_name:
        setting_list = [settingsHandler.get_setting(user.get('burner_sn'), setting_name)]
    else:
        setting_list = settingsHandler.get_settings(user.get('burner_sn'), user.get('role'))

    payload = {'settings': setting_list}

    return OkResponse(payload) if len(setting_list) > 0 else ConflictResponse(payload)

@accepted_roles(all_roles())
@JsonIn
def put(settingsToUpdate):
    user = authentication.get_current_user()
    res = settingsHandler.update_settings(settingsToUpdate, user.get('burner_sn'))
    return OkResponse(res)

@accepted_roles(all_roles())
def delete(setting_name = None):
    user = authentication.get_current_user()
    if setting_name is None and 'admin' in user.get('role'):
        settingsHandler.factory_reset_all(user.get('burner_sn'))
    else:
        settingsHandler.factory_reset(setting_name, user.get('burner_sn'))
    return get()
