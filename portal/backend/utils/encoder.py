import datetime, decimal

def simple_encoder(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        raise Exception("Cold not encode data %s of type %s" % (obj, type(obj)))


def escape(params):
    res = []
    for param in params:
        res.append(escape_string(param))
    return res


def escape_string(param):
    if type(param) == str:
        param = param.replace('%', '%%')
    return param