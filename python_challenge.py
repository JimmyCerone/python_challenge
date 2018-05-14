#!/usr/bin/python

import requests
# allows me to interact with the APIs

import re
# allows me to parse the file pretty efficiently

import json
# allows me to break down what I get from the api

UrlBase = 'http://api.ipstack.com/'
# url of the GeoIP api

key = '0e34684e50752e999974b9ed08c62875'
# key for the API - max of 10,000 requests for free version

text_file = "list_of_ips.txt"
# I ask the user for the name of the file (probably should just change this to the file name)
    
# I want this function to take in the text file and make a list based on spaces

# So quick update - we cannot split this based on spaces... not sure how to split
# this at all actually. There are instances of periods right after the IP, multiple
# IPs smashed together and more. So not a simple parse.

# So basically I think a rule that would always work is if something
# starts with a number. They didn't put any more numbers in there. 

# That said, that is not very general... I guess I could probably look up
# how folks parse for IPs...

# ok so I found a sick package called re which can help me parse through
# in a pretty general way for the format of IP addresses. This is what I will
# use to find all the IP addresses...

def ips(file_of_text):

	ip_list = list()
	
	giant_string = ""

	with open(text_file) as file:
	
		# ok so new strategy because I don't think re can take this 
		# all at once... I'm going to go line by line and make a giant string
		
		for line in file:
			
			giant_string += line
	
		# I think I will be unable to go line by line... There are multiline IPs...
		# Can I go through the document as a whole with Regex?
		# for line in file:
		ip_regex = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}', giant_string)
		
		# creates a file named ipFile which contains all the IP addresses found in the file
		f = open("ipFile.txt", "w")
		
		# This is apparently not a string... Need to check return type
		# returns a list, which should be easy to iterate over. 
		for ip in ip_regex:
			
			ip_list.append(ip)
			
			f.write("\n" + ip)
			
		f.close()
		
		# prints a list of all the IP addresses - can comment out later 
		# but helpful for a check
		# print ip_list
		
		# This allows the user to confirm that all IP addresses were found
		print "The number of IP addresses found in the document is: " + str(len(ip_list))
		
	return ip_list
	

	
# I want this function to take in the list and return all the IP addresses

	# I ended up folding this into the parser - which I think is just the best way to do it.

# I want this function to filter the IP addresses

# This set up seems cool but I'm concerned that I'm making a list of all IP addresses without filtering first
	# Actually not that hard to do - I'm fine with doing this every time.
	
# so all that is one thing... To prepare the data for GeoIP and RDAP lookup

# I found an API for GeoIP but not yet for RDAP

# So the goal is now to get the text files out (which I can do now) and perform a GeoIP look up

def geoIP(listOfIPs):

	# Since I have a limited number of calls I do this for one IP in the list
	# However, if I had an unlimited number I would use a for loop here to iterate
	# over the list of IPs... I am actually unsure though about this. It depends on 
	# how I want to filter... I think whatever way I wanted to filter I'd have to do that
	# I realize there are a few ways to filter. You can filter by the type of data you get
	# (field - location, country_code, etc) or by the values in the fields (Fishers, USA, country code = 355)
	# I am setting mine up to be the first, partly because I have a limited number of calls
	# and partly because I think that many of these IPs aren't real (at least the first wasn't)
	# and so it would be weird to check their fields.
	responses = list()
	# Ok so update, many of these IPs are real. So we are a go on the dictionary filtering method detailed in the filter method
	for x in range(0, 5): 
		
		responses.append(requests.get(UrlBase + listOfIPs[x] + "?access_key=" + key))
		# so I'm getting the html of the site back for some reason... 
		# fixed this by changing the base website I was pulling the API from (entered it in wrong initially)
	
	
	
	# filtering occurs here:
	# kind of weird but we append the rdap query to the GEO one.
	
	# grabs desired fields from GEOquery
	fields = GEOqueryFilter()
	# grabs desired fields from RDAP
	RDAP = RDAPqueryFilter()
	# adds all the RDAP fields individually
	for r in RDAP:
	
		fields.append(r)
		
	print fields
	
	for response in responses:
	
		for field in fields:
	
			print "The " + field + " is " + str(json.loads(response.content)[field]) + " for the IP address." 
	
		print "\n"
	# print response.content
	# I think my problem is here but I'm not sure what it is....
	# The problem was that I had the wrong url and the wrong key entry method...
	
	
	
# returns a list of the fields desired by the user from the GeoIP
	
def GEOqueryFilter():

	print "--------------GEOIP-------------------"

	print "Choose from the following list of fields the information you want to know about the IP address."
	
	print   "ip, " + "type, " + "continent_code, " + "continent_name, " + "country_code, " + "country_name, " + "region_code, " + "region_name, " + "city, " + "zip, " + "latitude, " + "longitude, " + "location"
	
	print "Enter each desired field separated by a single space. All letters should be lower cased."
	
	fields = raw_input()
	
	# Ok so change of plans, I think the filtering by the value of the field makes the 
	# most sense even if I can't really execute it because of my access limits with the API
	# So given that, I will need a dictionary holding the fields they care about and what they 
	# want to filter the field by
	
	list_of_fields = fields.split()
	
	return list_of_fields
	
	
def RDAPqueryFilter():
	
	# I am unsure how to do the rdap api so I will just copy the GeoIP stuff to here
	
	# Once I find an API for RDAP I will have to alter the fields...
	
	print "---------------------------RDAP-----------------------"
	
	print "Choose from the following list of fields the information you want to know about the IP address."
	
	print   "type, " + "continent_code, " + "continent_name, " + "country_code, " + "country_name, " + "region_code, " + "region_name, " + "city, " + "zip, " + "latitude, " + "longitude, " + "location"
	
	print "Enter each desired field separated by a single space. All letters should be lower cased."
	
	fields = raw_input()
	
	list_of_fields = fields.split(" ")
	
	return list_of_fields
	
	
ips(text_file)

geoIP(ips(text_file))

# I've never really done filtering before so I'm not sure what to do... 
# My best guess is to display all the fields that can be retrieved from RDAP
# and GeoIP then give them the option to type in what they want for each category

# Ok so slight problem, I only get 10,000 queries on the free API thing i was using for GeoIP
# So then I am going to have to test this like one thing at a time then do a big final test (maybe)
# No actually I will have to do lots of mini tests to allow Nick to do a full one. 