__author__ = 'rasmusletterkrantz'


from dao import tag_dao


def delete(tag_name, controller_ip):
    return tag_dao.delete_tag(tag_name, controller_ip)


def insert(tag):
    if tag_dao.add_tag(tag):
        print('Added a new tag')
        return True
    return False


def update(tag):
    print("trying to update tag")
    return tag_dao.update_tag(tag)



def get(id):
    return tag_dao.get(id)


def get_by_controller_id(controller_id):
    return tag_dao.get_by_controller(controller_id)


def get_all():
    return tag_dao.get_all()
