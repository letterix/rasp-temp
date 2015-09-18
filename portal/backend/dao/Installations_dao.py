import backend


def get(serial_number):
    sql = """SELECT * FROM `installations` where `serial_number` = %s;"""
    data = backend._query_for_one(sql, serial_number)
    return data;


def get_all(customer_name):
    sql = """SELECT * from installations WHERE customer = %s;"""
    return backend._query(sql, customer_name)


def get_customerless():
    sql = """SELECT * from installations WHERE customer IS NULL;"""
    return backend._query(sql)


def update(installation):
    sql = """UPDATE installations SET `name`= %s, `model` = %s, `customer` = %s WHERE `serial_number` = %s;"""
    return backend._exec(sql, installation.get('name'), installation.get('model'), installation.get('customer'), installation.get('serial_number'))


def register(installation):
     return backend._exec("""INSERT INTO installations(`serial_number`, `model`, `name`) VALUES(%s, %s, %s);""", installation['serial_number'], installation['model'], installation['name'])

def create(installation):
     return backend._exec("""INSERT INTO installations(`serial_number`, `model`, `name`, `customer`) VALUES(%s, %s, %s, %s);""", installation['serial_number'], installation['model'], installation['name'], installation['customer'])


def delete(serial_number):
    return backend._exec("""DELETE FROM installations WHERE `serial_number` = %s;""", serial_number)