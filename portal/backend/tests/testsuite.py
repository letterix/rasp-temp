import unittest
from tests import usertest
    
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(usertest.suite())
    return test_suite

if __name__ == "__main__":
    TEST_RUNNER = unittest.TextTestRunner(verbosity=2)
    TEST_SUITE = suite()
    TEST_RUNNER.run(TEST_SUITE)
