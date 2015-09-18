__author__ = 'rasmusletterkrantz'


from dao.base_dao import r_server
from redis.exceptions import RedisError

_HOLDING_REGISTER_TAG = '%MW'

def add_tag(tag):
    try:
        if validate_tag(tag):
            if r_server.sadd('controllers', tag['controller_ip']):
                print('Added a new controller')
            if r_server.sadd('tags:%s' % tag['controller_ip'], tag['name']):
                r_server.hset('tag:%s:%s' % (tag['controller_ip'], tag['name']), 'address', tag['address'])
                r_server.hset('tag:%s:%s' % (tag['controller_ip'], tag['name']), 'type', tag['type'])
                r_server.hset('tag:%s:%s' % (tag['controller_ip'], tag['name']), 'controller_ip', tag['controller_ip'])
                return True
        return False
    except RedisError:
        return False


def update_tag(tag):
    try:
        if validate_tag(tag):
            if not r_server.sadd('tags:%s' % tag['controller_ip'], tag['name']):
                r_server.hset('tag:%s:%s' % (tag['controller_ip'], tag['name']), 'address', tag['address'])
                r_server.hset('tag:%s:%s' % (tag['controller_ip'], tag['name']), 'type', tag['type'])
                r_server.hset('tag:%s:%s' % (tag['controller_ip'], tag['name']), 'controller_ip', tag['controller_ip'])
                return True
        return False
    except RedisError:
        return False


def delete_tag(tag_name, controller_ip):
    try:
        if r_server.sismember('tags:%s' % controller_ip, tag_name):
            print('removing tag: %s, with ip: %s' % (tag_name, controller_ip))
            r_server.srem('tags:%s' % controller_ip, tag_name)
            r_server.delete('tag:%s:%s' % (controller_ip, tag_name))
            if not r_server.smembers('tags:%s' % controller_ip):
                r_server.srem('controllers', controller_ip)
                print('No more tags for the controller, removing controller')
            return True
        else:
            return False
    except RedisError:
        return False

def get_tag(tag_name, controller_ip):
    try:
        if r_server.sismember('tags:%s' % controller_ip, tag_name):
            tag = {}
            tag['name'] = tag_name
            tag['address'] = r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'address')
            tag['type'] = r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'type')
            tag['controller_ip'] = r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'controller_ip')
            return tag
        else:
            return None
    except RedisError:
        return None

def get_controller_tags(controller_ip):
    try:
        tags = []
        for tag_name in r_server.smembers('tags:%s' % controller_ip):
            if r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'controller_ip') == controller_ip:
                tag = {}
                tag['name'] = tag_name
                tag['address'] = r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'address')
                tag['type'] = r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'type')
                tag['controller_ip'] = r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'controller_ip')
                tags.append(tag)
        return tags
    except RedisError:
        return None

def get_tags():
    try:
        tags = []
        for controller_ip in r_server.smembers('controllers'):
            for tag in get_controller_tags(controller_ip):
                tags.append(tag)
        return tags
    except RedisError:
        return None


def delete_controller_tags(controller_ip):
    try:
        tags = []
        for tag_name in r_server.smembers('tags:%s' % controller_ip):
            if r_server.hget('tag:%s:%s' % (controller_ip, tag_name), 'controller_ip') == controller_ip:
                tags.append(tag_name)
        for tag_name in tags:
            delete_tag(tag_name)
        return tags
    except RedisError:
        return None


def validate_tag(dict):
    """Address, Name and Controller """
    if dict and len(dict) >= 4:
        if dict['address'] and validate_address(dict['address']):
            if dict['name']:
                if dict['type']:
                    if dict['controller_ip'] and validate_ip(dict['controller_ip']):
                        return True
    return False

def validate_address(address):
    if address.startswith(_HOLDING_REGISTER_TAG) and 4 <= len(address) <= 8:
        return True
    else:
        return False

def validate_ip(ip):
    if isinstance(ip, str):
        if len(ip.split('.')) == 4:
            return True
        return False
