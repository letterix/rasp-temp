insert into users(role, username, password, salt, name, surname, email, phone)
values
    ('super_user', 'super', '55977cea079bab6a000c80303927f0f93f587e400f56ff3eab3ad869bfdb0f8cbf0397f1d96073432b7e1ccaeeab2d378d9f9f1d9f7b6062393cf9999e0bcd4d',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('master_admin', 'master_admin', '55977cea079bab6a000c80303927f0f93f587e400f56ff3eab3ad869bfdb0f8cbf0397f1d96073432b7e1ccaeeab2d378d9f9f1d9f7b6062393cf9999e0bcd4d',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('master_user', 'master_user', '55977cea079bab6a000c80303927f0f93f587e400f56ff3eab3ad869bfdb0f8cbf0397f1d96073432b7e1ccaeeab2d378d9f9f1d9f7b6062393cf9999e0bcd4d',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('admin', 'esbe_admin', '55977cea079bab6a000c80303927f0f93f587e400f56ff3eab3ad869bfdb0f8cbf0397f1d96073432b7e1ccaeeab2d378d9f9f1d9f7b6062393cf9999e0bcd4d',
        'bbe228e1fe274ed9982d7ee80bf410bf', 'Us', 'er', 'bla2@bla2.com', '0987654321'),
    ('user', 'esbe_user', '55977cea079bab6a000c80303927f0f93f587e400f56ff3eab3ad869bfdb0f8cbf0397f1d96073432b7e1ccaeeab2d378d9f9f1d9f7b6062393cf9999e0bcd4d',
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