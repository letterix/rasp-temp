import unittest
import sys
from tests import setup_testdb
import cherrypy
import json
sys.path.append('..')
import backend
from dao import AlarmDao, NewAlarmsDao, settings_dao, NewSettingsDao
import authentication
sys.path.append('../api')

backend.set_test()
setup_testdb.setup()


class TestUser(unittest.TestCase):

    BURNER_ID = "1234567890B"
    TYPE = "type_check"
    SETTING = {"setting_name" : "internal_pelletslevel_warning", "value" : "10.0"}

    def test_010_alarm_trigger(self):
        AlarmDao.create_alarm(self.BURNER_ID, self.TYPE, "error")
        new_alarms = NewAlarmsDao.get_all()
        self.assertEqual(1, len(new_alarms))
        inserted = new_alarms[0]

        real_alarm = AlarmDao.get_alarm(inserted['alarm_id'], self.BURNER_ID)
        self.assertEqual(real_alarm['type_key'], self.TYPE)

    def test_011_setting_trigger(self):
        settings_dao.update_setting(self.SETTING, self.BURNER_ID)
        new_settings = NewSettingsDao.get_all()
        self.assertEqual(1, len(new_settings))

        inserted = new_settings[0]

        real_setting = settings_dao.get_setting_by_name(self.BURNER_ID, self.SETTING['setting_name'])
        self.assertEqual(real_setting['burner_sn'], inserted['burner_sn'])
        self.assertEqual(real_setting['setting_name'], inserted['setting_name'])
        self.assertEqual(real_setting['value'], inserted['value'])

        self.SETTING['value'] = 666
        settings_dao.update_setting(self.SETTING, self.BURNER_ID)
        new_settings = NewSettingsDao.get_all()
        self.assertEqual(1, len(new_settings))

        inserted = new_settings[0]
        real_setting = settings_dao.get_setting_by_name(self.BURNER_ID, self.SETTING['setting_name'])
        self.assertEqual(real_setting['burner_sn'], inserted['burner_sn'])
        self.assertEqual(real_setting['setting_name'], inserted['setting_name'])
        self.assertEqual(real_setting['value'], inserted['value'])

    @classmethod
    def setUpClass(self):
        backend._exec("DELETE FROM new_alarms")
        backend._exec("DELETE FROM new_settings")
