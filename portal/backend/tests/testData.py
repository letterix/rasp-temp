import json

date, burner = "2013-10-10 10:10:10", "1234567890A"

ALARM_CREATE = {
    "id": 1,
    "burner_sn": burner,
    "method": "insert",
    "table": "alarms",
    "data": json.dumps({
        "acknowledged": 0,
        "date": date,
        "type_key": "ALARM_ERROR_LO",
        "burner_sn": burner,
        "severity": "error",
        "id": 7,
        'state_key': ''
    })
}
ALARM_UPDATE = {
    "id": 2,
    "burner_sn": burner,
    "method": "update",
    "table": "alarms",
    "data":json.dumps({
        "acknowledged": 1,
        "id": 1
    })
}
ALARM_DELETE = {
    "id": 3,
    "burner_sn": burner,
    "method": "delete",
    "table": "alarms",
    "data": json.dumps({
        "id": 1
    })
}

USER_CREATE_OK = {
    "id": 4,
    "burner_sn": burner,
    "method": "insert",
    "table": "users",
    "data": json.dumps({
        "username": "created",
        "role": "user",
        "email": "created@gmail.com",
        "name": "created@gmail.com",
        "surname": "created",
        "phone": "created",
        "burner_sn": burner,
        "password": "created",
        "salt": "created",
        "lang": 'en'
    })
}

USER_CREATE_FAIL = {
    "id": 5,
    "burner_sn": burner,
    "method": "insert",
    "table": "users",
    "data": json.dumps({ "username": "created"})
}

USER_UPDATE = {
    "id": 6,
    "burner_sn": burner,
    "method": "update",
    "table": "users",
    "data": json.dumps({
        "username": "username",
        "role": "updated_admin",
        "email": "updated_email",
        "name": "updated_name",
        "surname": "updated_surname",
        "phone": "updated_phone",
        "burner_sn": burner,
        "password": "updated_password",
        "salt": "updated_salt",
        "lang": 'se'
    })
}

USER_UPDATE_CONFLICT = {
    "id": 6,
    "burner_sn": burner,
    "method": "update",
    "table": "users",
    "data": json.dumps({
        "username": "conflict",
        "role": "updated_admin",
        "email": "updated_email",
        "name": "updated_name",
        "surname": "updated_surname",
        "phone": "updated_phone",
        "burner_sn": burner,
        "password": "updated_password",
        "salt": "updated_salt",
        "lang": "se"
    }),
    "prev": json.dumps({
        "username": "conflict",
        "role": "updated_admin",
        "email": "updated_email",
        "name": "updated_name",
        "surname": "updated_surname",
        "phone": "updated_phone",
        "burner_sn": burner,
        "password": "updated_password",
        "salt": "updated_salt",
        "lang": "se"
    })
}

SETTING_UPDATE = {
    "id": 7,
    "burner_sn": burner,
    "method": "update",
    "table": "settings",
    "data": json.dumps({
        "burner_sn": burner,
        "setting_name": "internal_pelletslevel_warning",
        "value": 20
    })
}

SETTING_UPDATE_CONFLICT = {
    "id": 7,
    "burner_sn": burner,
    "method": "update",
    "table": "settings",
    "data": json.dumps({
        "burner_sn": burner,
        "setting_name": "internal_pelletslevel_warning",
        "value": 70
    }),
    "prev": json.dumps({
        "burner_sn": burner,
        "setting_name": "internal_pelletslevel_warning",
        "value": 40
    })
}


USER_DELETE = {
    "id": 8,
    "burner_sn": burner,
    "method": "delete",
    "table": "users",
    "data": json.dumps({
        "username": "remove_me"
    })
}

ACK = {
    "ack": 1,
    "burner_sn": "1234567890A"
}

USER_CORRECTION_ACK = {
    "ack": 3,
    "burner_sn": "1234567890A",
    "correction": json.dumps({
        "username": "conflict",
        "role": "role",
        "email": "updated_email",
        "name": "updated_name",
        "surname": "updated_surname",
        "phone": "updated_phone",
        "burner_sn": burner,
        "password": "updated_password",
        "salt": "updated_salt",
        "lang": 'se'
    })
}

SETTING_CORRECTION_ACK = {
    "ack": 4,
    "burner_sn": "1234567890A",
    "correction": json.dumps({
        "burner_sn": burner,
        "setting_name": "internal_pelletslevel_warning",
        "value": 255
    })
}

