import backend

def get_log_for(installation, fromDate, toDate):
    sql =  """SELECT * FROM log WHERE installation = %s and `time` >= %s and `time` <= %s"""
    return backend._query(sql, installation, fromDate, toDate)

def get_last_entry(installation, controller_ip):
    sql = """SELECT * FROM log WHERE installation = %s AND controller_ip = %s ORDER BY `time` DESC LIMIT 1"""
    return backend._query_for_one(sql, installation, controller_ip)

def get_last_entry_by_name(installation, controller_ip, entry_name):
    sql = """SELECT * FROM log WHERE installation = %s AND name = %s AND controller_ip = %s ORDER BY `time` DESC LIMIT 1"""
    return backend._query_for_one(sql, installation, entry_name, controller_ip)

def create_log_entry(entry, installation):
    return backend._exec("""INSERT INTO log(`name`, `value`, `time`, `address`, `type`, `installation`, `controller_ip`) VALUES(%s,%s,%s,%s,%s,%s,%s)""", entry['name'], entry['value'], entry['time'], entry['address'], entry['type'], installation, entry['controller_ip'])







