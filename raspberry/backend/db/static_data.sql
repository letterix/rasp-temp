insert into installation(serial_number, model) values ('DUMMY', 'DUMMY');

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


INSERT INTO settings (installation, setting_name, `value`)  (SELECT 'DUMMY', setting_name, default_value FROM setting_types);


