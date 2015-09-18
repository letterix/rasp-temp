from dao import settings_dao, sync_queue_dao

def update_setting(setting, burner_sn, sync = True):
    print("update: ", setting)
    prev = settings_dao.get_setting_by_name(burner_sn, setting['setting_name'])
    updated = settings_dao.update_setting(setting, burner_sn)
    if updated and sync:
        sync = sync_queue_dao.insert_params(burner_sn, 'settings', 'update', setting, prev)
    return updated

def update_settings(settingsToUpdate, burner_sn):
    msg = []
    if type(settingsToUpdate) == list:
        for setting in settingsToUpdate:
            updated = update_setting(setting, burner_sn)
            msg.append({setting.get('setting_name'): updated})

    elif type(settingsToUpdate) == dict:
        updated = update_setting(settingsToUpdate, burner_sn)
        msg.append({settingsToUpdate.get('setting_name'): updated})
    else:
       msg.append("ERROR")
    return msg

def get_setting(burner_sn, setting_name):
    return settings_dao.get_setting_by_name(burner_sn, setting_name)

def get_settings(burner_sn, role):
    return settings_dao.get_settings(burner_sn, role)

def create_sync_entry_for(setting):
    sync_queue_dao.insert_params(setting['burner_sn'], 'settings', 'update', setting)

def factory_reset_all(burner_sn):
    settings = settings_dao.get_settings(burner_sn, 'admin')
    for setting in settings:
        setting['value'] = setting['default_value']
        update_setting(setting, burner_sn)

def factory_reset(setting_name, burner_sn):
    setting = get_setting(burner_sn, setting_name)
    default = settings_dao.get_default_for(setting_name)
    setting['value'] = default
    update_setting(setting, burner_sn)
