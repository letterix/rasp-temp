import unittest
import sys
from tests import setup_testdb
import cherrypy
import json
sys.path.append('..')
import backend
from dao import UserDao
import authentication
sys.path.append('../api')
from api import user

backend.set_test()
setup_testdb.setup()

class TestUser(unittest.TestCase):
    
    def test_010_post(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        user.post("username", "surname", "name", "1234567890", "password", "email@email.com")
        createduser = UserDao.get_user("username")
        self.assertEqual(createduser['name'], "name")
        self.assertEqual(createduser['number'], "1234567890")
        self.assertEqual(createduser['username'], "username")
        self.assertEqual(createduser['role'], "user")
        
    def test_011_post_duplicate(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        response = user.post("username", "surname", "name", "1234567890", "password", "email@email.com")
        self.assertEqual(response.content, '"User already exists"')
        
    def test_020_put(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        olduser = UserDao.get_user("username")
        self.assertEqual(olduser['email'], "email@email.com")
        
        user.put(olduser['id'], olduser['username'], olduser['surname'], olduser['name'], olduser['number'], olduser['password'], 'new@email.com')
        changeduser = UserDao.get_user("username")
        self.assertEqual(changeduser['name'], "name")
        self.assertEqual(changeduser['number'], "1234567890")
        self.assertEqual(changeduser['email'], "new@email.com")
        
    def test_030_get(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        response = user.get(None)
        self.assertEqual(len(json.loads(response.content)['users']), 4)
    
    def test_031_get_specific(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        response = user.get('username')
        self.assertEqual(json.loads(response.content)['name'], 'name')
        
    def test_032_get_non_existing(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        response = user.get('nonexisting')
        self.assertEqual(response.content, '"Could not find nonexisting"')
        
    def test_040_delete(self):
        global cherrypy
        cherrypy.session = {'roles': ['admin', 'planner', 'driver']}
        user.delete('username')
        deleteduser = UserDao.get_user("username")
        self.assertIsNone(deleteduser, "deleted user still exists")
        
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestUser))
    return test_suite
    
if __name__ == '__main__':
    unittest.main()