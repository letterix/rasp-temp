import time, datetime

def now():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

def to_current_timestmap(d):
    return d.strftime('%Y-%m-%d %H:%M:%S')

def datetime_to_unix(dt):
    return int((time.mktime(dt.timetuple()) + dt.microsecond/1000000.0)*1000)
