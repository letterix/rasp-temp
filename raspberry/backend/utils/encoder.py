import datetime, decimal

def simple_encoder(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        raise Exception("Cold not encode data %s of type %s" % (obj, type(obj)))
