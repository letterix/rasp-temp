#Database settings.
import os.path


current_dir = os.path.dirname(os.path.abspath(__file__))


LOCAL = True
CENTRAL = not LOCAL

RUN_SYNC_FREQUENCY = 15
SYNC_PING_FREQUENCY = 30
CHECK_ESBE_SETTINGS_FREQUENCY = 120
READ_LOG_VALUES_FREQUENCY = 15

SYNC = {
    'url': 'ws://127.0.0.1:1444/sync_ws'
    #'url': 'ws://141.255.189.241:1444/sync_ws'
}


DATABASE = {
    'path':  os.path.abspath(os.path.dirname(__file__)) + '/db/',
    'host': 'localhost',
    'dbname': 'liteDB',
    'user': 'kelmo',
    'password': 'kelmo'
}

TESTDATABASE = {
    'host': 'localhost',
    'dbname': 'liteDBTest',
    'user': 'kelmo',
    'password': 'kelmo'
}

SERIAL = {
    'port': '/dev/ttyUSB0'
}

CONF = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 1445,
        'tools.staticdir.on': True,
        'tools.staticdir.root': os.path.dirname(os.path.abspath(current_dir)),
        'tools.staticdir.dir': 'frontend/app',
        'tools.staticdir.content_types': {'js':  'application/javascript; charset=utf-8'},
        'tools.sessions.on': True,
        'tools.sessions.timeout': 180,
        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8'
    },
    '/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.abspath("favicon.ico")
    }
}
