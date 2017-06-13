
 
### umCustomerMgmt ###

Updates Customers in a Usage Meter server based on an input text file.

* Supports all UM 3.x Versions

___Sample Usage___ 


```
python umCustomerMgmt.py -s 10.134.3.240:8443  -t TOKHYCFE05BIHXAUJQJA1NVNRWKWI4EF5DS  -i /tmp/customers.tsv -d
```

___Sample Output___


```
UM Version: 3.5
Successfully opened input file.  

Error Updating customer Coke (2022bb46-e685-4202-b5ba-45fef1934076) msg=  is not a valid country code. See http://www.iso.org/iso/home/standards/country_codes/.
Error Updating customer CustomerA (9517e566-3119-4fb5-b6c4-466960a60c75) msg=  is not a valid country code. See http://www.iso.org/iso/home/standards/country_codes/.
Error Updating customer CustomerB (23b466f4-bbe4-4f6e-8d15-f7e8458ef0c1) msg=  is not a valid country code. See http://www.iso.org/iso/home/standards/country_codes/.
Error Updating customer CustomerZ msg= 

Processing complete.
	Created Customers  0
	Updated Customers: 1
	Deleted Customers  1
	Error Count: 4
```
