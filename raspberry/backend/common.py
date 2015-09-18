import json, datetime, decimal, cherrypy
from collections import namedtuple

Response = namedtuple('response', 'status content')
OkResponse = lambda msg: Response('200 Ok', json.dumps(msg, default=datahandler))
CreatedResponse = lambda msg: Response('201 Created', json.dumps(msg, default=datahandler))
MalformedResponse = lambda msg: Response('400 Malformed Request', json.dumps(msg, default=datahandler))
UnauthorizedResponse = lambda msg: Response('401 Unauthorized',json.dumps( msg, default=datahandler))
NotFoundResponse = lambda msg: Response('404 Not found', json.dumps(msg, default=datahandler))
UnsupportedResponse = lambda msg: Response('405 Method Not Allowed', json.dumps(msg, default=datahandler))
ConflictResponse = lambda msg: Response('409 Conflict', json.dumps(msg, default=datahandler))
ErrorResponse = lambda msg: Response('500 Internal Server Error', json.dumps(msg, default=datahandler))

def redirect(url):
    redirectObj = cherrypy.HTTPRedirect(url)
    redirectObj.urls[0] = url
    raise redirectObj


URL_INDEX = '/index.html'

def datahandler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError("Cannae serialize %s of type %s" % (obj,type(obj)))


class JsonIn(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, *args, **kwargs):

        cl = cherrypy.request.headers['Content-Length']
        rawbody = cherrypy.request.body.read(int(cl))
        body_string = rawbody.decode("utf-8")
        if body_string:
            object = json.loads(body_string)
            return self.f(object)
        else:
            print("JSON!!", body_string)
            return ConflictResponse("MISSING DATA")
