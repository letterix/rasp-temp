insert into users(role, username, password, salt, name, surname, email, phone)
values
    ('master_admin', 'master', '55977cea079bab6a000c80303927f0f93f587e400f56ff3eab3ad869bfdb0f8cbf0397f1d96073432b7e1ccaeeab2d378d9f9f1d9f7b6062393cf9999e0bcd4d',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321');

insert into customers(name)
values
    ('master');

insert into assignees(`user`,customer)
values
    ('master', 1);

INSERT INTO setting_types(setting_name, min_value, max_value, default_value, role, `group`, type)
VALUES
    ('ROOM_SET_TEMP1',5,30.0,20.0,'user',1, 'temp'),
    ('ROOM_SET_TEMP2',5,30.0,20.0,'user',1, 'temp'),
	('WATER_MIN_SET_TEMP',5.0,95.0,20.0,'user',1, 'temp'),
	('WATER_MAX_SET_TEMP',5,95.0,45.0,'user',1, 'temp'),
	('WATER_TEMP',5,95.0,45.0,'user',1, 'temp'),
	('WATER_SET_TEMP1',5,95.0,45.0,'user',1, 'temp'),
	('WATER_SET_TEMP2',5,95.0,45.0,'user',1, 'temp'),

	('OUT_TEMP_TABLE_0',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_1',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_2',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_3',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_4',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_5',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_6',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_7',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_8',5,30.0,20.0,'user',2, 'temp'),
	('OUT_TEMP_TABLE_9',5,30.0,20.0,'user',2, 'temp'),

    ('CRC_P',0,9,5,'user',3, 'triple'),
    ('CRC_H',0,9,5,'user',3, 'triple'),
    ('CRC_S',0,9,5,'user',3, 'triple'),
    ('CRB_P',0,9,5,'user',3, 'triple'),
    ('CRB_H',0,9,5,'user',3, 'triple'),
    ('CRB_I',0,9,5,'user',3, 'triple'),
    ('CRC_TD',0,9,5,'user',3, 'triple'),
    ('CRC_N',0,9,5,'user',3, 'triple'),
    ('CRD_ADAPTION',0,9,5,'user',3, 'triple'),
    ('CRD_U',0,9,5,'user',3, 'triple');











