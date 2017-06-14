
import unittest, sys

# Sample usage
# cd umsamples
# python test/testUmCustomerMgmt.py 10.134.3.240:8443 TOKHYCFE05BIHXAUJQJA1NVNRWKWI4EF5DS

# Unit tests may execute in parallel, so cannot depend on one another
# For example create and fetch need to be in the same unit test or they will fail when run in parallel.
# Unit tests should be stand alone

class TestUmCustomerMgmt(unittest.TestCase):
    "A few simple tests for TestUmCustomerMgmt"

    def __init__(self, testname, UMserver, UMtoken):

        super(TestUmCustomerMgmt, self).__init__(testname)
        self.UMserver = UMserver
        self.UMtoken = UMtoken
        self.mgr = UMCustomerMgmt(self.UMserver, self.UMtoken)

    def test_create_get_update_delete(self):
        print "test_create_get_update_delete - Create"
        result = self.mgr.create_customer('CustomerZ', 'US', '43017')
        self.assertTrue(result[0], result[1])

        print "test_create_get_update_delete - Get"
        result = self.mgr.get_customer('CustomerZ')
        self.assertTrue(result[0], result[1])
        self.assertTrue("<name>CustomerZ</name>" in result[1])

        print "test_create_get_update_delete - Update"
        result = self.mgr.update_customer('CustomerZ', 'US', '94304')
        self.assertTrue(result[0], result[1])

        print "test_create_get_update_delete - Verify Update"
        result = self.mgr.get_customer('CustomerZ')
        self.assertTrue(result[0], result[1])
        self.assertTrue("<postalCode>94304</postalCode>" in result[1])

        print "test_create_get_update_delete - Delete"
        result = self.mgr.delete_customer('CustomerZ')
        self.assertTrue(result[0],result[1])


    def test_delete_unknown_customer(self):

        print "test_delete_unknown_customer"
        result = self.mgr.delete_customer('CustomerQ')
        self.assertFalse(result[0])

    def test_get_unknown_customer(self):

        print "test_get_unknown_customer"
        result = self.mgr.delete_customer('CustomerQ')
        self.assertFalse(result[0])


if __name__ == '__main__':
    
    if __package__ is None:
        # called from umsamples folder with python test/testUmCustomerMgmt.py
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from src.umsamples.umCustomerMgmt import UMCustomerMgmt
    else:
        # called from umsamples with python -m test.testUmCustomerMgmt  (no.py)
        from src.umsamples.umCustomerMgmt import UMCustomerMgmt

    import sys
    server = sys.argv[1]
    token = sys.argv[2]

    print "Testing against " + server 

    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestUmCustomerMgmt)

    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(TestUmCustomerMgmt(test_name, server, token))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
