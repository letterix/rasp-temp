insert into users(role, username, password, salt, name, surname, email, phone)
values
    ('super_user', 'super', 'e581ee15ff0626b1e46fdf32433159a4ff135a79ca60557f6c891254673e0d3e2b11e4cf0899023975fe034d7cb0235be30e09cfb2ef25a740486e3cb4d49f21',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('master_admin', 'master_admin', 'e581ee15ff0626b1e46fdf32433159a4ff135a79ca60557f6c891254673e0d3e2b11e4cf0899023975fe034d7cb0235be30e09cfb2ef25a740486e3cb4d49f21',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('master_user', 'master_user', 'e581ee15ff0626b1e46fdf32433159a4ff135a79ca60557f6c891254673e0d3e2b11e4cf0899023975fe034d7cb0235be30e09cfb2ef25a740486e3cb4d49f21',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('admin', 'esbe_admin', 'e581ee15ff0626b1e46fdf32433159a4ff135a79ca60557f6c891254673e0d3e2b11e4cf0899023975fe034d7cb0235be30e09cfb2ef25a740486e3cb4d49f21',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('user', 'esbe_user', 'e581ee15ff0626b1e46fdf32433159a4ff135a79ca60557f6c891254673e0d3e2b11e4cf0899023975fe034d7cb0235be30e09cfb2ef25a740486e3cb4d49f21',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321');

insert into customers (name)
values
    ('master'),
    ('Esbe'),
    ('Cuatro');

insert into assignees (`user`, customer)
values
    ('esbe_admin',2),
    ('esbe_user',2);

insert into installations (`serial_number`, `name`, model, customer)
values ('66002174487292', 'DaMachine', 'pi', 2);

insert into controllers (installation, name, ip)
values ('66002174487292', 'kelmo plc', '192.168.0.1');
