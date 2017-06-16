
 
### umCustomerMgmt ###

Performs a batch Update of Customers in a Usage Meter server based on an input text file.

#### Input file format ####

The file format is based on the Customer export file exported by Usage Meter.

One customer per line, values delimited with a tab character,

Each line contains either one value or three values.

- Customers to be added or updated contain three values, a customer name, country and postal code, each separted by \t

- Customers to be deleted contain a single value of customer name followed by a new line.

Lines starting with a # characater are comment lines and are ignored

A line beginning with # followed by the word Rules, indicate that the remainder of the file contains rule lines,

When a line beginning with # Rules is encountered, the rest of the input file lines are ignored.

___Sample File___

```
# vCloud Usage Meter Customer Export
# Version: 1
# Customers
# Name  Country Postal Code

# Create new customer
CustomerA       US      43017

# Create new customer
CustomerB       US      43017

# Create new customer
CustomerC       US      43017

# Update customer
CustomerB       US      94304

# Delete customers
CustomerA
CustomerB
CustomerC

# Rules
# Example rule: Exact string folder match for abc for customer CloudCo
# CloudCo               Folder  Exact String    abc
# Customer      vCenter Object Type     Value Type      Value
```

___Usage___

umManageCustomers.py -s 127.0.0.1:8443  -t umtoken  -i  inputFile [-d] 

-s  - Usage Meter Appliance and port

-t  - API Token from Usage Meter for API authentication

-i  - customer input file containing customer data in tab separated format

-d  - debug [Optional]


___Sample Usage___ 

```
python umCustomerMgmt.py -s 10.134.3.240:8443  -t TOKHYCFE05BIHXAUJQJA1NVNRWKWI4EF5DS  -i /tmp/customers.tsv 
```

___Sample Output___


```
Connect to https://10.134.3.240:8443/um/
UM Version: 3.5
Successfully opened input file.  

Created:  CustomerA
Created:  CustomerB
Created:  CustomerC
Updated:  CustomerB
Deleted:  CustomerA
Deleted:  CustomerB
Deleted:  CustomerC

Processing complete.
Created: 3
Updated: 1
Deleted: 3
Errors:  0

```
