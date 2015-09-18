#Database settings.
import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))


LOCAL = False
CENTRAL = not LOCAL

RUN_SYNC_FREQUENCY = 15
SYNC_PING_FREQUENCY = 30

DATABASE = {
    'host': 'localhost',
    'dbname': 'modwatch_dev',
    'user': 'modwatch_dev',
    'password': 'modwatch_dev'
}

TESTDATABASE = {
    'host': 'localhost',
    'dbname': 'kelmotest',
    'user': 'kelmotest',
    'password': 'kelmotest'
}

CONF = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 1444,
        'tools.staticdir.on' : True,
        'tools.staticdir.root': os.path.dirname(os.path.abspath(current_dir)),
        'tools.staticdir.dir' : 'frontend/app',
        'tools.staticdir.content_types' : {'js':  'application/javascript; charset=utf-8'},
        'tools.sessions.on' : True, 
        'tools.sessions.timeout' : 180,
        'tools.encode.on': True,
        'tools.encode.encoding': 'utf-8',
    },
    '/favicon.ico': {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': os.path.abspath("favicon.ico")
    }
}
