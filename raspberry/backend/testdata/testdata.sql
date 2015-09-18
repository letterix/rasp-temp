insert into burners(serial_number, model) values
    ('1234567890A', 'PX22'),
    ('1234567890B', 'PX22')
;

insert into users (role, username, password, salt, name, surname, email, phone, burner_sn) values
    ('role', 'username', 'password', 'salt', 'name', 'surname', 'email', 'phone', '1234567890A'),
    ('role', 'remove_me', 'password', 'salt', 'name', 'surname', 'email', 'phone', '1234567890A'),
    ('role', 'conflict', 'conflict_pass', 'conflict_salt', 'conflict', 'conflict', 'conflict@conflict', 'phone', '1234567890A')
;

INSERT INTO setting_types(setting_name, min_value, max_value, default_value, role) VALUES
	('internal_pelletslevel_warning', 0, 1000.0, 100, 'user')
;

insert into settings(burner_sn, setting_name, `value`) VALUES
    ('1234567890A', 'internal_pelletslevel_warning', 100),
    ('1234567890B', 'internal_pelletslevel_warning', 100)
;

insert into sync_queue(id, burner_sn, `table`, `method`, `data`) VALUES
  (1, '1234567890A', 'alarms', 'insert', '{"type_key": "TIME_LIMIT_SHUTDOWN1","date": "2013-11-04 10:10:10","id": 14283,"severity": "error","burner_sn": "1234567890A","acknowledged": 0}'),
  (2, '1234567890A', 'alarms', 'insert', '{"type_key": "TIME_LIMIT_SHUTDOWN2","date": "2001-01-01 01:01:01","id": 10000,"severity": "error","burner_sn": "1234567890A","acknowledged": 1}'),
  (3, '1234567890A', 'users', 'update', 'blabla'),
  (4, '1234567890A', 'settings', 'update', 'blabla')
;

insert into alarms(id, burner_sn, type_key, severity, acknowledged, state_key) VALUES
    (1, '1234567890A', 'EXTERNAL_PELLETS_ALARM_LEVEL', 'warning', 0, '')
;
