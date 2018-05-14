# python_challenge
Takes a text file with IP addresses and allows the user to look up geographic information about the addresses.

The goal of the following program is to: 

read a given set of IPs, perform Geo IP and RDAP lookups, and accept a query to filter results.

Basically, the program allows you to input a file containing IP addresses and then learn about certain 
geographic characteristics of the IP address (which you can specify). 

The program is written in Python 2.7. 

The program is best run in the command line with no arguments necessary. 

In the future, an optional argument for the name of the text file containing the IP addresses can be added. 

Currently, the program is only able to perform the reading and Geo IP functions. 

The program utilizes the Regular Expression package (re) to read the file and identify the IP adresses contained
in the file. The IP addresses are written to a file (ipFile.txt) for later use if necessary. 

An adequate RDAP lookup API was not found and therefore only GeoIP lookup can be performed. A limitation of the 
GeoIP API used means a low volume of IP addresses can be looked up at any one time. The maximum overall lookups with the 
given key is 10,000 and as a result the program is currently configured to look up 5 IP's at a time (though this can be increased
through editing the source code). 

The query to filter results can also be improved. Currently the system is fairly weak. The user is limited to choosing the field to 
be returned from the GeoIP look up. So, for example, a user can ask for the latitude of each (of the 5) IP addresses returned. The 
user specifies the field, but is not currently able to specify a desired value for the field, which basically means they cannot filter
results at this stage. 

The user is offered a choice of fields and prompted to choose which they want displayed from the command line (taken in using raw_input). 

To build out a solid filter, I think that a dictionary would be required, to hold the category a user wants to search within and the desired
result. Then in the loop for the JSON, the desired result could be checked against the GeoIP / RDAP feedback. 

Questions for consideration: 

- How can RDAP lookup be performed? Are there existing APIs for this? Can ARIN be used? Is that the most efficient option?

- Is a dictionary the most efficient way to handle the filtering process?
