
import unittest, sys, requests.exceptions
from cStringIO import StringIO
from contextlib import contextmanager


# Sample usage
# cd umsamples
# python test/testUmCustomerMgmt.py 10.134.3.240:8443 TOKHYCFE05BIHXAUJQJA1NVNRWKWI4EF5DS

# Unit tests may execute in parallel, so cannot depend on one another
# For example create and fetch need to be in the same unit test or they will fail when run in parallel.
# Unit tests should be stand alone

class TestUmCustomerMgmt(unittest.TestCase):
    "A few simple tests for TestUmCustomerMgmt"

    def __init__(self, testname, UMserver, UMtoken, inputFile):

        super(TestUmCustomerMgmt, self).__init__(testname)
        self.UMserver = UMserver
        self.UMtoken = UMtoken
        self.mgr = UMCustomerMgmt(self.UMserver, self.UMtoken)
    

    def test_create_get_update_delete(self):
        print "Test Create"
        result = self.mgr.create_customer('CustomerZ', 'US', '43017')
        self.assertTrue(result[0], result[1])

        print "Test Get"
        result = self.mgr.get_customer('CustomerZ')
        self.assertTrue(result[0], result[1])
        self.assertTrue("<name>CustomerZ</name>" in result[1])

        print "Test Update"
        result = self.mgr.update_customer('CustomerZ', 'US', '94304')
        self.assertTrue(result[0], result[1])

        print "Test Verify Update"
        result = self.mgr.get_customer('CustomerZ')
        self.assertTrue(result[0], result[1])
        self.assertTrue("<postalCode>94304</postalCode>" in result[1])

        print "Test Delete"
        result = self.mgr.delete_customer('CustomerZ')
        self.assertTrue(result[0],result[1])


    def test_delete_unknown_customer(self):
        print "Test Delete Unknown Customer"
        result = self.mgr.delete_customer('CustomerQ')
        self.assertFalse(result[0])
        self.assertTrue("Error Deleting customer:" in result[1])

    def test_update_unknown_customer(self):
        print "Test Update Unknown Customer"
        result = self.mgr.update_customer('Cus', 'US', '94304')
        self.assertFalse(result[0])
        self.assertTrue("Error Updating customer:" in result[1])

    def test_update_invalid_country_code(self):
        # create for update
        result = self.mgr.create_customer('CustomerVV', 'US', '43017')
        self.assertTrue(result[0], result[1])

        print "Test Update Invalid Country Code"
        result = self.mgr.update_customer('CustomerVV', 'USZ', '94304')
        self.assertFalse(result[0])
        self.assertTrue("is not a valid country code" in result[1])

        # delete after test
        result = self.mgr.delete_customer('CustomerVV')
        self.assertTrue(result[0],result[1])

    def test_create_invalid_country_code(self):
        print "Test Create Invalid Country Code"
        result = self.mgr.create_customer('CustomerU', 'USZ', '94304')
        self.assertFalse(result[0])
        self.assertTrue("Error Creating customer:" in result[1])
        self.assertTrue("is not a valid country code" in result[1])

    def test_get_unknown_customer(self):

        print "Test Get Unknown Customer"
        result = self.mgr.get_customer('CustomerQ')
        self.assertFalse(result[0])
        self.assertTrue("Error Retrieving customer: " in result[1])

    def test_bad_server(self):

        print "Test Bad Server Name"
        with self.assertRaises(requests.exceptions.ConnectionError):
            UMCustomerMgmt("unknownServer:8443", "ANYTOKEN")
    
    # Tests input file and check stdout values
    def test_and_capture(self):
        print "Test Process Input File: " + inputFile

        args = ['-s', self.UMserver, '-t', self.UMtoken, '-i', inputFile]

        # Note: Kept returning TypeError: 'NoneType' object is not callable' since main() did not have sys.exit()        
        with capture(src.umsamples.umCustomerMgmt.main, args) as output:

          self.assertTrue("Created: 1" in output, "Incorrect Created count: " + "\n " + output)
          self.assertTrue("Updated: 1" in output, "Incorrect Updated count: " + "\n " + output)
          self.assertTrue("Deleted: 1" in output, "Incorrect Deleted count: " + "\n " + output)
          self.assertTrue("Errors:  2" in output, "Incorrect Errors  count: " + "\n " + output)



@contextmanager
def capture(command, *args, **kwargs):
  out, sys.stdout = sys.stdout, StringIO()
  try:
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
  finally:
    sys.stdout = out


if __name__ == '__main__':
    
    if __package__ is None:
        # called from umsamples folder with python test/testUmCustomerMgmt.py
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from src.umsamples.umCustomerMgmt import UMCustomerMgmt
        import src.umsamples.umCustomerMgmt
    else:
        # called from umsamples with python -m test.testUmCustomerMgmt  (no.py)
        from src.umsamples.umCustomerMgmt import UMCustomerMgmt
        import src.umsamples.umCustomerMgmt

    import sys
    server = sys.argv[1]
    token = sys.argv[2]
    inputFile = sys.argv[3]

    print "Testing against " + server 

    test_loader = unittest.TestLoader()
    test_names = test_loader.getTestCaseNames(TestUmCustomerMgmt)

    suite = unittest.TestSuite()
    for test_name in test_names:

        suite.addTest(TestUmCustomerMgmt(test_name, server, token, inputFile))

    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
