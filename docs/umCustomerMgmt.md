
 
### umReporter ###

Supports the unattended collection of Monthly Usage Report Data from a Usage Meter Server for a specified range of months. Connects to the UM Server using the UM API.  The report data is saved to a specified comma separated file.  The csv file is Excel compatible and can be imported into a spreadsheet. 

* Supports all UM 3.x Versions
* Removes empty columns in reports to simplify output

___Sample Usage___ 

Request MUR data from 20161201 - 20170301 with -r option - descending date sort.

```
python umReporter.py -s 10.161.235.45:8443 -t TOKD1STSEVXLAGURFXXIGFJWQHMQZJIFKMH -b 20161101 -e 20170301 -o /tmp/report_35.csv -r 
```

___Sample Output___

(Note: Bundles output varies by UM Version)

```
Month,Std GB,Prem GB,Prem Plus GB

201405,0,951,0
     
201404,0,891,0
     
201403,0,837,0
     
201402,0,754,0
     
201401,0,734,0
     
201312,0,733,0
```
