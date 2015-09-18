from dao import sync_queue_dao

def delete(id, installation):
    return sync_queue_dao.delete(id, installation)

def insert(sync):
    return sync_queue_dao.insert(sync)

def get(id):
    return sync_queue_dao.get_by_id(id)

def get_by_burner_sn(installation):
    return sync_queue_dao.get_by_installation(installation)

def get_all():
    return sync_queue_dao.get_all()

def set_attempt_time(sync_item):
    sync_queue_dao.set_attempt_time(sync_item['id'], sync_item['installation'])
