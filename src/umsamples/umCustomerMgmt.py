#!/usr/bin/python2.7
#############
# This utility updates Customers in a UM Server using values from a tab delimited file.
#
# The file format is based on the Customer export file exported by Usage Meter.
# One customer per line, Values in the line are delimited with a tab character,
# Each line contains either one value or three values.
# Customers to be added or updated contain three values, a customer name, country and postal code, each separted by \t
# Customers to be deleted contain a single value of customer name followed by a new line. 
# Lines starting with a # characater are comment lines and are ignored
# A line beginning with # followed by the word Rules, indicate that the remainder of the file contains rule lines,
# When a line beginning with # Rules is encountered, the rest of the input file lines are ignored.
#
# The utility runs from the command line as shown below.
# Prior to execution, an API token must be generated using the Usage Meter UI and the value passed using the -t flag.
# The optional -d file enables debug output to stdout
#
# python umCustomerMgmt.py -s 10.134.3.240:8443  -t TOKHYCFE05BIHXAUJQJA1NVNRWKWI4EF5DS  -i ../../test/customers.tsv -d
#
# Supports Usage Meter Versions 3.2, 3.3, 3.4 and 3.5
# Requires: Python 2.7.10
# Author: Bob Webster June 2017
#
#############

import requests
import sys, getopt
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from httplib import HTTPConnection
import csv
import traceback
import xmltodict
import logging

class UMCustomerMgmt:

    def __init__(self, UMserver, UMtoken, debug=False):

        self.debug = debug
        self.UMserver = UMserver
        self.UMtoken = UMtoken

        # Connect to server
        self.create_session()

        # Get all customers from UM Server and build a name - key dictionary
        self.custKeyDict = self.get_all_customer_ids()


    def find_between(self,  s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""



    # Get all customers and build a dictionary of customer name to id.
    def get_all_customer_ids(self):

        # Using Session, token no longer required, note put/post calls return 403 without Content-Type: application/xml
        headers = {'x-usagemeter-authorization': self.UMtoken, 'Content-Type': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
        keyDict = {}
        
   
        customerList = requests.get("https://" + self.UMserver  + "/um/api/customers", headers=self.headers, verify=False, timeout=10);

        if self.debug:
            print customerList.status_code

        if customerList.status_code != 200:
          raise NameError("Http Error: " + str(customerList.status_code)  + 
                          " Unable to retrieve customer list from UM Server")

        if self.debug:
            print "Customer List:"
            print customerList.content

        # Parse XML into Dict

        doc = xmltodict.parse(customerList.content)
        if self.debug:
            print "XML Doc as Dict " + str(doc)

        # Build customer name - id dictionay
   
        for c in doc['customers']['customer']:
              keyDict[c['name']] = c['id']

        if self.debug:
            print "Name-id Dictionary"
            print str(keyDict)

        return keyDict


    # Return a single customer record from the UM Server
    # Returns a tuple of success (True or False) and message
    # message contains the customer in XML format or an error message if status is False
    def get_customer(self, name):

        # Get customer

        try:
          id = self.custKeyDict[name]

          customer = requests.get("https://" + self.UMserver  + "/um/api/customer/" + id, headers=self.headers, verify=False, timeout=10);

          if self.debug:
              print "https://" + self.UMserver  + "/um/api/customer/" + str(id)
              print customer.status_code
              print customer.content

          if customer.status_code != 200:
             return (False, "Error Retrieving customer: " + name  + " http Status: " +  str(customer.status_code) +
                    " msg= " + customer.content)

          return (True, customer.content)

        except KeyError:
             return (False, "Error Retrieving customer: " + name + " not in customer-key list.")




    # Update an existing customer record in the UM Server
    # Returns a tuple of success (True or False) and message
    # message contains the customer id in string format or an error message if status is False
    def update_customer(self, name, country, postalCode):


        # Update customer

        body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + \
               "<customer xmlns=\"http://www.vmware.com/UM\">\n" + \
               "<name>" + name + "</name>\n" + \
               "<country>" + country + "</country>\n" + \
               "<postalCode>" + postalCode  + "</postalCode>\n" + \
               "</customer>\n"
               
        try:

          id = self.custKeyDict[name]

          customer = requests.put("https://" + self.UMserver  + "/um/api/customer/" + id, headers=self.headers, data=body, verify=False, timeout=10);

          if self.debug:
              print "https://" + self.UMserver  + "/um/api/customer/" + str(id)
              print body
              print customer.status_code
              print customer.content

          if customer.status_code != 200:
              return (False, "Error Updating customer: " + name  + " http Status: " +  str(customer.status_code) +
                    " msg= " + customer.content)

          return (True, str(id))

        except KeyError:
              return (False, "Error Updating customer: " + name + " not in customer-key list.")




    # Create an new customer record in the UM Server
    # Returns a tuple of success (True or False) and message
    # message contains the id of the new customer in string format or an error message if status is False
    def create_customer(self, name, country, postalCode):

        # Create customer

        body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + \
               "<customer xmlns=\"http://www.vmware.com/UM\">\n" + \
               "<name>" + name + "</name>\n" + \
               "<country>" + country + "</country>\n" + \
               "<postalCode>" + postalCode  + "</postalCode>\n" + \
               "</customer>\n"
         


        customer = requests.post("https://" + self.UMserver  + "/um/api/customer", headers=self.headers, data=body, verify=False, timeout=10);

        if self.debug:
            print "https://" + self.UMserver  + "/um/api/customer/" 
            print body
            print customer.status_code
            print customer.content

        if customer.status_code != 201:
             return (False, "Error Creating customer: " + name  + " http Status: " +  str(customer.status_code) +
                    " msg= " + customer.content)

        id = self.find_between( customer.content, '<id>', '</id>' )
        if self.debug:
            print "New Customer id: " + str(id)

        if len(id) == 0:
            return (False, "Error: Unable to retrieve id for new Customer named " + name)

        # update customer key map with new entry
        self.custKeyDict[name] = id

        # for debug, prove we can get it
        if self.debug:
            result = self.get_customer(name)
            print "Fetch newly created Customer: " + str( result[0]) + " : " + str (result[1])

        return (True, id)




    # Delete an existing customer record in the UM Server
    # Returns a tuple of success (True or False) and message
    # message contains the customer id in string format or an error message if status is False
    def delete_customer(self, name):

        # Delete customer
               
        try:

          id = self.custKeyDict[name]

          customer = requests.delete("https://" + self.UMserver  + "/um/api/customer/" + id, headers=self.headers, verify=False, timeout=10);

          if self.debug:
              print "https://" + self.UMserver  + "/um/api/customer/" + str(id)
              print customer.status_code
              print customer.content

          if customer.status_code != 204:
              return (False, "Error Deleting customer: " + name  + " http Status: " +  str(customer.status_code) +
                    " msg= " + customer.content)


          #  remove customer from key list
          del self.custKeyDict[name]
  
          return (True, str(id))


        except KeyError:
          return (False, "Error Deleting customer: " + name + "  not in customer-key list.")

    # Retrieve UM Banner page to determine UM Version 
    # setup SSL for different versions of Usage Meter and define a retry count for all http calls
    # Raises requests.exceptions.SSLError or requests.exceptions.RequestException or requests.exceptions.ConnectTimeout on failure
    def create_session(self):

        self.headers = {'x-usagemeter-authorization': self.UMtoken,  'Content-Type': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }


        # Supress associated InsecureRequestWarning for UM with Self Signed Cert
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        if self.debug:

          #logging.basicConfig(level=logging.DEBUG)
          self.debug_requests_on()

        #
        # Get UM version from banner page title -  <title>VMware vCloud Usage Meter 3.5</title>
        # Also verifies that SSL handshake works, adjust cyphers for earlier versions of UM
        #
        try:
             banner = requests.get("https://" + self.UMserver  + "/um/", headers=self.headers, verify=False, timeout=10);
             v = self.find_between( banner.content, 'VMware vCloud Usage Meter ', '</title>' )
             print "Connect to " + "https://" + self.UMserver  + "/um/"
             print "UM Version: " + v
        except requests.exceptions.SSLError as e:

           # For UM 3.2, 3.3 or 3.4 Versions
           # ("bad handshake: Error([('SSL routines', 'tls_process_ske_dhe', 'dh key too small')],)     
           # Must adjust ssl Cyphers and try again 
           requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
           try:
              requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
           except AttributeError:
              # no pyopenssl support used / needed / available
               pass

           banner = requests.get("https://" + self.UMserver  + "/um/", headers=self.headers, verify=False, timeout=10);
           v = self.find_between( banner.text, 'VMware vCloud Usage Meter ', '</title>' )
           print "UM Version: " + v

        #   Use alternative transport adapter to set retry count
        #   So rety if    requests.exceptions.ConnectionError
             
        requests.Session().mount('https://' + self.UMserver, HTTPAdapter(max_retries=5))


    # Returns a dictionary of counters, records updatedCount, createdCount, deletedCount and errorCount
    # or an exception on failure
    def process_file(self, inputFile):

        updatedCount =0
        createdCount =0
        deletedCount =0
        errorCount =0

        # open input file

        csv.register_dialect('tab', delimiter='\t')
        f_input_file = open(inputFile, 'r')

        print "Successfully opened input file.  \n"

        try:
            reader = csv.reader(f_input_file, dialect='tab')

            # Read input file, ignoring rules section and comments
            for record in reader:
                     if len(record) == 0:
                          continue
                     if record[0].startswith('# Rules'):
                          break
                     elif record[0].startswith('#'):
                          continue
                     else:
                          # Existing customer?
                          if record[0] in self.custKeyDict:
                               
                               # delete request? Name and no other columns?
                               if len(record) == 1:
                                    result = self.delete_customer(record[0])
                                    if result[0]:
                                       print( "Deleted:  " + record[0])
                                       deletedCount = deletedCount + 1
                                    else:
                                        print( "Delete Error: " + record[0] + " " + record[1])
                                        errorCount = errorCount + 1
                               # Bad record
                               else:
                                    if len(record) == 2:
                                        print( "Bad Record missing \\t: " + str(record))
                                        errorCount = errorCount + 1
                                    else:
                                          # Update -                    customerName, Country, PostalCode
                                          result = self.update_customer( record[0], record[1], record[2])
                                          if result[0]:
                                              print( "Updated:  " + record[0])
                                              updatedCount = updatedCount + 1
                                          else: 
                                              print( "Update Error: " + record[0] + " " + record[1])
                                              errorCount = errorCount + 1

                          # Create Customer since unknown customer
                          else: 
                               # unless one field, then an unknown delete
                               if len(record) == 1:
                                   print( "Delete Error: " + record[0] + " does not exist and cannot be deleted.")
                                   errorCount = errorCount + 1
                               else:
                                   #  Create -                    customerName, Country, PostalCode
                                    result = self.create_customer(record[0], record[1], record[2])
                                    if result[0]:
                                       print( "Created:  " + record[0])
                                       createdCount = createdCount + 1
                                    else:
                                       errorCount = errorCount + 1
                                       print( "Create Error: " + record[0] + " " + record[1])

            return  {'createdCount': createdCount, 'updatedCount': updatedCount, 'deletedCount': deletedCount, 'errorCount': errorCount}

        # return any exception
        finally:
            f_input_file.close()



    def debug_requests_on(self):
        '''Switches on logging of the requests module.'''
        HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    def usage():

          print 'Usage umManageCustomers.py -s 127.0.0.1:8443  -t TOK3W1T0BZZGBQ4CUIEFSUF4B3RDX3ETUDT  -i  ./customerFile.tsv -d' 
          print ' -s  = Usage Meter Appliance and port'
          print ' -t  = API Token from Usage Meter for API authentication'
          print ' -i  = customer input file containing customer data in tab separated format'
          print ' -d  = debug'


######################
### Main
######################

def main(argv):

    # Process command line input
 
    debug = False

    try:
       opts, args = getopt.getopt(argv,"hds:t:i:")
    except getopt.GetoptError:
       usage()
       sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
         usage()
         sys.exit()
      elif opt in ("-s"):
         UMserver = arg
      elif opt in ("-t"):
         UMtoken = arg
      elif opt in ("-i"):
         inputFile = arg
      elif opt in ("-d"):
         debug = True 
    try:
     UMserver
     UMtoken
     inputFile
    except NameError:
     print "Insufficient parameters"
     usage()
     sys.exit(3)

    try:

        mgr = UMCustomerMgmt(UMserver, UMtoken, debug)
        results = mgr.process_file(inputFile)

        print "\nProcessing complete."
        print "Created: " + str(results['createdCount'])
        print "Updated: " + str(results['updatedCount'])
        print "Deleted: " + str(results['deletedCount'])
        print "Errors:  " + str(results['errorCount'])

        sys.stdout.flush()
    

    except (Exception) as error:
        sys.stderr.write( "Error: Processing Error \n")
        sys.stderr.write(str(error) + "\n")
        print traceback.format_exc()


if __name__ == "__main__":
   main(sys.argv[1:])

