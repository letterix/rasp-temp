#!/usr/bin/python
#  -*- coding: UTF-8 -*-

import cherrypy, api, os.path, inspect, authentication, config
#import requests
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws.sync_ws_socket import SyncWsSocket

from cherrypy.process.plugins import Monitor
from sync.SyncManager import run as run_sync
from ws.sync_heartbeat import send_ping
from dao import UserDao
from handlers import installationHandler, assigneesHandler

from common import *
from utils.timeUtil import *
import uuid, time, datetime
from cherrypy.lib.static import serve_file

SECONDS_PER_DAY = 86400
COOKIE_LENGTH = SECONDS_PER_DAY * 30
COOKIE_EXPIRE = COOKIE_LENGTH + round(time.time())
COOKIE_NAME = 'cookie_id'
current_dir = os.path.dirname(os.path.abspath(__file__))

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
        if 'user' not in cherrypy.session:
            raise cherrypy.HTTPError("401 Unauthorized")

        # To fix the unicode parameter encoding
        args = [arg.encode('latin1').decode('utf-8') for arg in args]

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
            return ConflictResponse(KEY_API_ERROR)

    @cherrypy.expose
    def cookie(self):
        request_cookie = cherrypy.request.cookie
        cookie_val = request_cookie.get(COOKIE_NAME).value.split('|')

        if len(cookie_val) == 2:
            username, cookie_id = cookie_val
            user = UserDao.get_user(username)

            if user.get('cookie_id') and user.get('cookie_expire'):
                if user['cookie_id'] == cookie_id and datetime_to_unix(user.get('cookie_expire')) > time.time():
                    authentication.login(cherrypy.session, user)
                    return OkResponse('ok')
        return ConflictResponse('error')

    @cherrypy.expose
    def login(self, username=None, password=None, remember_me=False):
        print(remember_me)
        if username and password:
            user = authentication.check_password(username, password)
            if user:
                user = authentication.login(cherrypy.session, user)

                if remember_me:
                    username, cookie_id = user.get('username'), uuid.uuid4().hex
                    self.setCookie( "%s|%s" % (username, cookie_id))
                    cookie_expire_timestamp = datetime.datetime.fromtimestamp(COOKIE_EXPIRE).strftime('%Y-%m-%d %H:%M:%S')
                    UserDao.update_cookie_id(cookie_id, cookie_expire_timestamp, username)

                self.index();
            else:
                try:
                    self.unsetCookie()
                except:
                    pass
                redirect('/login.html?failed=true')
        else:
            redirect(URL_LOGIN)

    @cherrypy.expose
    def logout(self):
        user = authentication.get_current_user()
        if user:
            authentication.logout(cherrypy.session)
            UserDao.delete_cookie(user.get('username'))
            self.usetCookie()
        redirect(URL_LOGIN)

    @cherrypy.expose
    def index(self):
        if authentication.is_logged_in(cherrypy.session):
            user = authentication.get_current_user()
            if authentication.is_master(user):
                redirect(URL_MASTER)
            else:
                customers = assigneesHandler.get_customers(user.get('username'))
                #Normal users can only be assigned to one customer.
                if customers:
                    customer = customers.pop()
                    redirect(URL_USER + str(customer.get('customer')))
                else:
                    redirect(URL_LOGIN)
        else:
            redirect(URL_LOGIN)

    @cherrypy.expose
    def master(self):
        if authentication.is_master_logged_in(cherrypy.session):
            redirect(URL_MASTER)
        else:
            redirect(URL_LOGIN)

    @cherrypy.expose
    def alarms_ws(self):
        handler = cherrypy.request.ws_handler

    @cherrypy.expose
    def sync_ws(self):
        handler = cherrypy.request.ws_handler
                                                                                                                           #TODO: finns filen redan flytta den och lägg på siffra bakom. max 5 sparade filer.
                                                                                                                            #TODO: 1 -> 2 , 2 -> 3 5-> inget
    @cherrypy.expose
    def upload_log_file(self,myFile,serial_number):

        if installationHandler.get(serial_number):
            size = 0
            for x in range(1,6):
                print("loops" + str(x))
                if os.path.isfile(myFile.filename + "." + str(x)) is True:
                    x +=1
                elif os.path.isfile(myFile.filename + "." + str(x)) is False and x > 1:
                    file = open(myFile.filename + "." + str(x), "w+")
                    data = open(myFile.filename + "." + str(x-1))
                    file.write(data.read())
                    file.close()
                    return myFile
                else:
                    file = open(myFile.filename + "." + str(x), "w+")
                    while True:
                        data = myFile.file.read(8192)
                        file.write(str(data))
                        if not data:
                            break
                        size += len(data)
                        file.close()
                        break
                    return myFile
        else:
            raise cherrypy.HTTPError('404', 'Unregistered device.')

    @cherrypy.expose
    def log_file_exists(self,filePath):
        if authentication.is_logged_in(cherrypy.session):
            try:
               with open(os.path.abspath(current_dir) + '\\\\' + filePath):
                    return OkResponse("Ok")
            except IOError:
               raise cherrypy.HTTPError('404', 'File does not exist.')
        else:
            return ErrorResponse("You must login to see log files")


    @cherrypy.expose
    def download_log(self, filePath):
        if authentication.is_logged_in(cherrypy.session):
            return serve_file(os.path.abspath(current_dir) + '\\\\' + filePath, "application/x-download", "attachment")
        else:
            return ErrorResponse("You must login to download the log file")


def get_handlers(package):
    handlers = {}

    for member_name, member in [module for module in inspect.getmembers(package)
        if inspect.ismodule(module[1])]:
            print("Adding handler %s" % member_name)
            handlers[member_name] = member
    return handlers

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
Monitor(cherrypy.engine, send_ping, frequency=config.SYNC_PING_FREQUENCY).subscribe()

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
