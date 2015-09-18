import sys, unittest, json, backend
from utils import timeUtil
from tests import setup_testdb, testData
sys.path.append('..')
sys.path.append('../api')
from dao import sync_queue_dao, AlarmDao, settings_dao, UserDao, NewAlarmsDao, NewSettingsDao
from sync import SyncManager
from unittest.mock import MagicMock
import config
backend.set_test()
setup_testdb.setup()

class TestSync(unittest.TestCase):

    callNumber = 0

    def test_001_onMessage_insert_alarm_ok(self):
        num_alarms_before = len(AlarmDao._get_all())
        alarm_msg = testData.ALARM_CREATE
        date, burner = testData.date, testData.burner

        SyncManager.onMessage(alarm_msg)
        alarms_after = AlarmDao._get_all()
        newest = len(alarms_after) -1

        self.assertEquals(len(alarms_after), num_alarms_before + 1)
        self.assertEquals(timeUtil.to_current_timestmap(alarms_after[newest]['date']), date)
        self.assertEquals(alarms_after[newest]['burner_sn'], burner)
        self.assertEquals(alarms_after[newest]['acknowledged'], 0)

    def test_002_onMessage_update_alarm_ok(self):
        alarm_update = testData.ALARM_UPDATE

        alarm_before = AlarmDao.get_alarm(json.loads(alarm_update['data'])['id'], testData.burner)
        self.assertEquals(alarm_before['acknowledged'], 0)

        SyncManager.onMessage(alarm_update)

        alarm_after = AlarmDao.get_alarm(json.loads(alarm_update['data'])['id'], testData.burner)
        self.assertEquals(alarm_after['acknowledged'], 1)

    def test_003_onMessage_delete_alarm_ok(self):
        alarm_delete = testData.ALARM_DELETE
        data = json.loads(alarm_delete['data'])

        alarm_before = AlarmDao.get_alarm(data['id'], testData.burner)
        self.assertIsNotNone(alarm_before)

        print(alarm_delete, (type(alarm_delete)))
        SyncManager.onMessage(alarm_delete)

        alarm_after = AlarmDao.get_alarm(data['id'], testData.burner)
        self.assertIsNone(alarm_after)


    def test_004_onMessage_update_setting_ok(self):
        setting_update = testData.SETTING_UPDATE
        setting_data = json.loads(setting_update['data'])
        setting_name, setting_val = setting_data['setting_name'], setting_data['value']

        setting_before = settings_dao.get_setting_by_name(testData.burner, setting_name)
        self.assertEquals(setting_before['value'], 100)
        config.LOCAL = False
        SyncManager.onMessage(testData.SETTING_UPDATE)

        setting_after = settings_dao.get_setting_by_name(testData.burner, setting_name)
        self.assertEquals(setting_after['value'], setting_val)


    def test_005_onMessage_create_user_ok(self):
        num_users_before = len(UserDao.get_all())
        user_template = testData.USER_CREATE_OK
        user_data = json.loads(user_template['data'])
        SyncManager.onMessage(user_template)
        num_users_after = len(UserDao.get_all())

        user_created = UserDao.get_user(user_data['username'])
        self.assertEquals(num_users_after, num_users_before + 1)
        self.assertEquals(user_created['username'], user_data['username'])

    def test_006_onMessage_create_user_fail(self):
        num_users_before = len(UserDao.get_all())
        SyncManager.onMessage(testData.USER_CREATE_FAIL)
        num_users_after = len(UserDao.get_all())
        self.assertEquals(num_users_after, num_users_before)

    def test_007_onMessage_update_user_ok(self):
        user_update = testData.USER_UPDATE
        config.LOCAL = False
        user_before = UserDao.get_user(json.loads(user_update['data'])['username'])
        SyncManager.onMessage(user_update)
        user_after = UserDao.get_user(json.loads(user_update['data'])['username'])

        self.assertNotEquals(user_before['email'], user_after['email'])
        self.assertNotEquals(user_before['surname'], user_after['surname'])
        self.assertNotEquals(user_before['name'], user_after['name'])
        self.assertNotEquals(user_before['phone'], user_after['phone'])
        self.assertNotEquals(user_before['password'], user_after['password'])
        self.assertNotEquals(user_before['salt'], user_after['salt'])

        self.assertEquals(user_before['role'], user_after['role'])
        self.assertEquals(user_before['username'], user_after['username'])
        self.assertEquals(user_before['burner_sn'], user_after['burner_sn'])

    def test_008_onMessage_delete_user_ok(self):
        user_delete = testData.USER_DELETE
        user_data = json.loads(user_delete['data'])
        user_before = UserDao.get_user(user_data['username'])
        self.assertIsNotNone(user_before)

        SyncManager.onMessage(user_delete)

        user_after = UserDao.get_user(user_data['username'])
        self.assertIsNone(user_after)


    def test_009_onAck_remove_syncRow(self):
        sync_item = sync_queue_dao.get_by_id(1)
        num_sync_rows_before = len(sync_queue_dao.get_all())
        self.assertTrue(sync_item['id'] == 1)

        SyncManager.onMessage(testData.ACK)
        num_sync_rows_after = len(sync_queue_dao.get_all())

        self.assertEquals(num_sync_rows_after, num_sync_rows_before -1)
        sync_item = sync_queue_dao.get_by_id(1)
        self.assertIsNone(sync_item)

    def test_010_test_not_accept_user_update(self):

        user_update_conflict = testData.USER_UPDATE_CONFLICT
        user_conflict_data = json.loads(user_update_conflict['data'])
        user_conflict_prev = json.loads(user_update_conflict['prev'])
        user_before = UserDao.get_user(user_conflict_data['username'])
        self.assertNotEqual(user_before, user_conflict_prev)

        config.LOCAL = True

        SyncManager.send_correction_ack = MagicMock(return_value="ok")
        SyncManager.onMessage(user_update_conflict)

        user_after = UserDao.get_user(user_conflict_data['username'])

        self.assertEqual(user_before, user_after)
        SyncManager.send_correction_ack.assert_called_with(user_update_conflict['id'], user_update_conflict['burner_sn'], user_before)

    def test_011_test_not_accept_settings_update(self):
        settings_conflict = testData.SETTING_UPDATE_CONFLICT


        setting_before = settings_dao.get_setting_by_name(settings_conflict['burner_sn'], json.loads(settings_conflict['data'])['setting_name'])
        self.assertNotEqual(json.loads(settings_conflict['prev']), setting_before)
        config.LOCAL = True

        SyncManager.send_correction_ack = MagicMock(return_value="ok")
        SyncManager.onMessage(settings_conflict)

        setting_after = settings_dao.get_setting_by_name(settings_conflict['burner_sn'], json.loads(settings_conflict['data'])['setting_name'])

        self.assertEqual(setting_before, setting_after)
        SyncManager.send_correction_ack.assert_called_with(settings_conflict['id'], settings_conflict['burner_sn'], setting_before)


    def test_012_test_user_correction_ack(self):

        user_conflict_ack = testData.USER_CORRECTION_ACK
        correction = json.loads(user_conflict_ack['correction'])
        user_before = UserDao.get_user(correction['username'])
        self.assertNotEqual(correction, user_before)

        SyncManager.onMessage(user_conflict_ack)

        user_after = UserDao.get_user(correction['username'])
        self.assertEqual(correction, user_after)



    def test_013_test_settings_correction_ack(self):

        settings_correction_ack = testData.SETTING_CORRECTION_ACK
        correction = json.loads(settings_correction_ack['correction'])

        setting_before = settings_dao.get_setting_by_name(settings_correction_ack['burner_sn'], correction['setting_name'])
        self.assertNotEqual(correction, setting_before)

        SyncManager.onMessage(settings_correction_ack)

        setting_after = settings_dao.get_setting_by_name(settings_correction_ack['burner_sn'], correction['setting_name'])
        self.assertEqual(correction, setting_after)

    def test_014_test_read_new(self):
        sync_entries = sync_queue_dao.get_all()
        self.assertEqual(1, len(sync_entries))

        new_alarms = NewAlarmsDao.get_all()
        self.assertEqual(1, len(new_alarms))

        new_settings = NewSettingsDao.get_all()
        self.assertEqual(1, len(new_settings))

        SyncManager.sendMessage = MagicMock(return_value="ok")
        SyncManager.run()

        new_alarms = NewAlarmsDao.get_all()
        self.assertEqual(0, len(new_alarms))

        new_settings = NewSettingsDao.get_all()
        self.assertEqual(0, len(new_settings))

        sync_entries = sync_queue_dao.get_all()
        self.assertEqual(3, len(sync_entries))




    def test_015_test_receive_message_not_adding_new_sync_entry(self):
        backend._exec("""DROP TRIGGER IF EXISTS alarm_after_insert;""");
        backend._exec("""DROP TRIGGER IF EXISTS settings_after_update;""");
        config.LOCAL = False
        sync_entries = sync_queue_dao.get_all()
        self.assertEqual(3, len(sync_entries))
        new_alarms = NewAlarmsDao.get_all()
        self.assertEqual(0, len(new_alarms))
        new_settings = NewSettingsDao.get_all()
        self.assertEqual(0, len(new_settings))

        sql = """DELETE FROM alarms"""
        backend._exec(sql)
        SyncManager.onMessage(testData.ALARM_CREATE)
        SyncManager.onMessage(testData.SETTING_UPDATE)

        new_alarms = NewAlarmsDao.get_all()
        self.assertEqual(0, len(new_alarms))
        new_settings = NewSettingsDao.get_all()
        self.assertEqual(0, len(new_settings))
        sync_entries = sync_queue_dao.get_all()
        self.assertEqual(3, len(sync_entries))

        pass


    @classmethod
    def setUpClass(self):
        backend._exec("DELETE FROM new_alarms")
        backend._exec("DELETE FROM new_settings")