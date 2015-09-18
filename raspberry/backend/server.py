import cherrypy, api, os.path, inspect, config, datetime
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws.sync_ws_socket import SyncWsSocket

from cherrypy.process.plugins import Monitor
from sync.SyncManager import run as run_sync
from ws.sync_ws_client import *
from ws.sync_heartbeat import send_ping
from handlers.read_log_values import read_all_parameters
from handlers import installationHandler
from ws.sync_users import LAST_RECIVED_PING

from common import *
from utils.timeUtil import *
import uuid, time, datetime

SECONDS_PER_DAY = 86400
COOKIE_LENGTH = SECONDS_PER_DAY * 30
COOKIE_EXPIRE = COOKIE_LENGTH + round(time.time())
COOKIE_NAME = 'cookie_id'

class Root(object):
    """Server application root"""
    test_index = 0

    def setCookie(self, value):
        cherrypy.response.cookie[COOKIE_NAME] = value
        cherrypy.response.cookie[COOKIE_NAME]['path'] = '/'
        cherrypy.response.cookie[COOKIE_NAME]['max-age'] = COOKIE_LENGTH
        cherrypy.response.cookie[COOKIE_NAME]['version'] = 1
    setCookie.exposed = True

    def usetCookie(self):
        cherrypy.response.cookie[COOKIE_NAME] = ''
        cherrypy.response.cookie[COOKIE_NAME]['max-age'] = 0
    setCookie.exposed = True

    @cherrypy.expose
    def api(self, target, *args, **kwargs):
        method = cherrypy.request.method.lower()

        """REST API handler"""
        if HANDLERS.get(target):
            handler = getattr(HANDLERS[target], method)
            response = handler(*args, **kwargs)

            if hasattr(handler, 'binary'):
                cherrypy.response.headers['Content-Type'] = handler.content_type
                cherrypy.response.headers['Content-Disposition'] = handler.content_disposition
                return response

            cherrypy.response.headers['Content-Type'] = 'application/json; charset=utf-8'

            cherrypy.response.status = response.status
            return response.content.encode('utf-8')
        else:
            print("Conflict")
            return ConflictResponse("Method not found")


    @cherrypy.expose
    def index(self):
        redirect(URL_INDEX)


    @cherrypy.expose
    def sync_ws(self):
        handler = cherrypy.request.ws_handler

def get_handlers(package):
    handlers = {}

    for member_name, member in [module for module in inspect.getmembers(package) 
        if inspect.ismodule(module[1])]:
            print("Adding handler %s" % member_name)
            handlers[member_name] = member
    return handlers

#To trigger new devices to set correct serial number before "workers" below does it at the same time
installation = installationHandler.get_installation()
print("installation is: ", installation.get('serial_number'))

LAST_RECIVED_PING['ping'] = datetime.datetime.now()

HANDLERS = get_handlers(api)

if False: #if SSL is needed
    CFG_DIR = ""
    SSL_CRT = os.path.join(CFG_DIR, 'ssl/domain.se.crt')
    SSL_KEY = os.path.join(CFG_DIR, 'ssl/domain.se.key')
    SSL_BUNDLE = os.path.join(CFG_DIR, 'ssl/ssl_bundle.pem')
    cherrypy.server.ssl_certificate = SSL_CRT
    cherrypy.server.ssl_private_key = SSL_KEY
    cherrypy.server.ssl_certificate_chain = SSL_BUNDLE
    cherrypy.server.ssl_module = 'pyopenssl'

WebSocketPlugin(cherrypy.engine).subscribe()
Monitor(cherrypy.engine, run_sync, frequency=config.RUN_SYNC_FREQUENCY).subscribe()
Monitor(cherrypy.engine, check_sync_ws, frequency=config.RUN_SYNC_FREQUENCY).subscribe()
Monitor(cherrypy.engine, send_ping, frequency=config.SYNC_PING_FREQUENCY).subscribe()
Monitor(cherrypy.engine, read_all_parameters, frequency=config.READ_LOG_VALUES_FREQUENCY).subscribe()

cherrypy.tools.websocket = WebSocketTool()

config.CONF['/sync_ws'] = {
    'tools.websocket.on': True,
    'tools.websocket.handler_cls': SyncWsSocket,
}

ROOT = Root()

cherrypy.engine.autoreload.unsubscribe()
cherrypy.engine.timeout_monitor.unsubscribe()
cherrypy.quickstart(ROOT, '/', config.CONF)

cherrypy.engine.stop()
