#!/usr/bin/python2.7
#############
# This utility retrieves specific bundle data from a usage meter server using the usage meter api.
# Not all bundle types are returned, The subset of bundles returned were selected to support the analysis of differences between UM versions.
# 
# The utility runs from the command line.
# An input range of report months can be specified using a begindate and enddate.
# The resulting report data is written to an output file in tab separated format which can be easily imported into excel.
#
# Supports Usage Meter Versions 3.2, 3.3, 3.4 and 3.5
# Requires: Python 2.7.10
# Author: Bob Webster April 2017
#   
# Prior to execution, an API token must be generated using the Usage Meter UI and the value passed with the -t flag.
#
# Test Sample 3.5
# python umCustomerMgmt.py -s 10.134.3.240:8443  -t TOKHYCFE05BIHXAUJQJA1NVNRWKWI4EF5DS  -i /tmp/customers.tsv -d
#
#
# Author: Bob Webster
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




def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def usage():

      print 'Usage umManageCustomers.py -s 10.32.51.xxx:8443  -t TOK3W1T0BZZGBQ4CUIEFSUF4B3RDX3ETUDT  -i  ./customerFile.tsv -d' 
      print ' -s  = Usage Meter Appliance and port'
      print ' -t  = API Token from Usage Meter for API authentication'
      print ' -i  = customer input file containing custmoers in tab separated format'
      print ' -d  = debug'


def getAllCustomerIds(UMserver, headers, debug):

    # Get list of customers

    try:
      customerList = requests.get("https://" + UMserver  + "/um/api/customers", headers=headers, verify=False, timeout=10);

      if debug:
          print customerList.status_code

      if customerList.status_code == 401:
          print ("Server returned Unauthorized: Invalid api token?")
          sys.exit(3)

      if debug:
          print customerList.text

      # Parse XML into Dict

      doc = xmltodict.parse(customerList.content)
      print "Doc " + str(doc)

      # Build customer name - id dictionay
      keyDict = {}
      for c in doc['customers']['customer']:
            keyDict[c['name']] = c['id']

      print str(keyDict)

    except requests.exceptions.Timeout:
          print "Unable to access server, timeout"
          sys.exit(4)

    return keyDict

def getCustomer(UMserver, headers, id, debug):


    # Get customer

    try:
      customer = requests.get("https://" + UMserver  + "/um/api/customer/" + id, headers=headers, verify=False, timeout=10);

      if debug:
          print customer.status_code

      if customer.status_code == 401:
          print ("Server returned Unauthorized: Invalid api token?")
          sys.exit(3)

      if debug:
          print customer.content


    except requests.exceptions.Timeout:
          print "Unable to access server, timeout"
          sys.exit(4)


def updateCustomer(UMserver, headers, id, name, country, postalCode, debug):


    # Update customer

    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" + \
           "<customer xmlns=\"http://www.vmware.com/UM\">\n" + \
           "<name>" + name + "</name>\n" + \
           "<country>" + country + "</country>\n" + \
           "<postalCode>" + postalCode  + "</postalCode>\n" + \
           "</customer>\n"
   #   "<customer xmlns=\"http://www.vmware.com/UM\">\n" + \
           
    try:
      print "https://" + UMserver  + "/um/api/customer/" + id
      print body

      customer = requests.put("https://" + UMserver  + "/um/api/customer/" + id, headers=headers, data=body, verify=False, timeout=10);

      if debug:
          print customer.status_code

      if customer.status_code == 401:
          print ("Server returned Unauthorized: Invalid api token?")
          sys.exit(3)

      if debug:
          print customer.content


    except requests.exceptions.Timeout:
          print "Unable to access server, timeout"
          sys.exit(4)

def debug_requests_on():
    '''Switches on logging of the requests module.'''
    HTTPConnection.debuglevel = 1

    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

######################
### Main
######################

def main(argv):

    headers = "";
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



    # Supress associated InsecureRequestWarning for UM with Self Signed Cert
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    if debug:

      #logging.basicConfig(level=logging.DEBUG)
      debug_requests_on()

    # Get UM version from banner page title -  <title>VMware vCloud Usage Meter 3.5</title>
    try:
         banner = requests.get("https://" + UMserver  + "/um/", headers=headers, verify=False, timeout=10);
         v = find_between( banner.text, 'VMware vCloud Usage Meter ', '</title>' )
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
       try:    
           banner = requests.get("https://" + UMserver  + "/um/", headers=headers, verify=False, timeout=10);
           v = find_between( banner.text, 'VMware vCloud Usage Meter ', '</title>' )
           print "UM Version: " + v
       except requests.exceptions.SSLError as e:
           print "http.requests ssl error: " + str(e)

    except requests.exceptions.RequestException as e:
       print "http.requests error: " + str(e)
       sys.exit(2)


    if v.startswith( '3.2' ):
       UMversion = '3.2'
    elif v.startswith( '3.3'):  
       UMversion = '3.3'
    elif v.startswith( '3.4'):
       UMversion = '3.4'
    elif v.startswith( '3.5'):
       UMversion = '3.5'
    else: 
       print ("Error: Could not determine UM Version. Is server a UM Appliance? ")
       print ("Suggestion: Use Browser to validate login to UM Server UI is successful.")
       sys.exit(2)

   #   Use alternative transport adapter to set retry count
   #   http://stackoverflow.com/questions/15431044/can-i-set-max-retries-for-requests-request
   #   So retries happen if    requests.exceptions.ConnectionError
         
    session = requests.Session()
    session.mount('https://' + UMserver, HTTPAdapter(max_retries=5))

    # Put calls return 403 without Content-Type: application/xml
    headers = {'x-usagemeter-authorization': UMtoken, 'Content-Type': 'application/xml', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

    # Get all customers and build name - key list

    custKeyDict = getAllCustomerIds(UMserver, headers, debug)


    
    # open input file
    try:
       csv.register_dialect('tab', delimiter='\t')

       f_input_file = open(inputFile, 'r')

    except (Exception) as error:
        print "Error: Unable to open specified input file."
        print(error)
        sys.exit(4)

    print "Successfully opened file.  \n"

    try:
        reader = csv.reader(f_input_file, dialect='tab')

        for row in reader:
                 if row[0].startswith('# Rules'):
                      break
                 elif row[0].startswith('#'):
                      next(reader)
                 else:
                      print "row is " + str(row)
                      print "\tCustomer " + row[0] + " Key is " + custKeyDict[row[0]] 


                     # getCustomer(UMserver, headers, custKeyDict[row[0]], debug)

        updateCustomer(UMserver, headers, "4", "CustomerC", "US", "43017", debug)
        getCustomer(UMserver, headers, "4", debug)

    except (Exception) as error:
        print "Error: Processing Error "
        print(error)
        print traceback.format_exc()
        sys.exit(4)

    finally:
        f_input_file.close()




   ###############
   ## Get reports
   ###############

 #  if   UMversion == "3.2":
 #        metaDataDict = process_32_reports(UMserver, UMtoken, beginDateTime, countMonths, outputFile, descendingsort, debug)

 #  elif UMversion == "3.3": 
 #        metaDataDict = process_33_reports(UMserver, UMtoken, beginDateTime, countMonths, outputFile, descendingsort, debug)

 #  elif UMversion == "3.4": 
 #        metaDataDict = process_34_reports(UMserver, UMtoken, beginDateTime, countMonths, outputFile, descendingsort, debug)

 #  elif UMversion == "3.5": 
 #        metaDataDict = process_35_reports(UMserver, UMtoken, beginDateTime, countMonths, outputFile, descendingsort, debug)

 #  else: 
 #       print "Unknown UM Version, " + UMversion + " exiting."
 #       sys.exit(4)


if __name__ == "__main__":
   main(sys.argv[1:])
