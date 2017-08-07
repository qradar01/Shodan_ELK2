#!/usr/bin/env python
# this script is for testing the shodan API functionality
# and the ultimate goal of querying the Shodan Database to determine if any
# IoT devices with an IP address are publicly visible.
#
# SYNTAX shodan.py 'IP LIST FILE'
#
# QCL 7/07/2014 Version 1.7

import shodan
import sys
import time
import types #this module is really useful to boolean evaluate the type() of what shodan query returns using isinstance().
import socket
import json

UDP_IP = "127.0.0.1"
UDP_PORT = 1999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SHODAN_API_KEY = “KEY”
api = shodan.Shodan(SHODAN_API_KEY)

def query_shodan(term):
	try:
		shodan_dict = api.host(term)
		return shodan_dict

	except shodan.APIError, e:
		return "Err0r: %s IP=%s" % (e, term) #I specify the string 'Err0r' as a way to detect this exception later in the program.

def conditional_logstash(dict):
	if "Err0r" in dict:
		return False
	elif isinstance(dict, types.DictType) == False: #this is more of an edge-case error checker; I don't think shodan queries can return anything except an Error or a dict.
		return False
	elif isinstance(dict, types.NoneType) == True:
		return False
	else:
		return True

def serialized_dict(dict):
	json_string = json.dumps(dict)
	return json_string

print "-------------------\nStarting Program\n-------------------"

#infile = sys.argv[1]
infile = "/home/elk/shodan/2build/IP.txt"
with open(infile) as fp:
	for line in fp:
		ip_query_result = query_shodan(line)
		time.sleep(1.5) #keep this here or program will spam shodan!
		print "\n[+] Querying Shodan for %s" % line
		if conditional_logstash(ip_query_result) == True:
			try:
				print "\n[+] Sending\n"
				dict_json = serialized_dict(ip_query_result)
				sock.sendto(dict_json, (UDP_IP, UDP_PORT))
				time.sleep(1)
			except IOError:
				print "\nUNDEFINED CONNECTION ERROR ENCOUNTERED."
		else:
			continue
sock.close()
print "------------------\nEnd Program\n------------------"






#changes from 0.6 to 0.7: moving the 'for pairing in shodan_dict' loop into the try block because
# if the API fails, the value being returned for query_shodan (host) was null, and then being called
# by this for loop without ever having been assigned values because the API failed.
# 	Changes between 0.7 -> 0.8: debugging various typos, starting to understand the data structure
# of the dict returned by shodan, so I know how to pull out relevant information and display it in the
# program's output.
#	V0.8->0.9: gave up trying to understand the data structure of the dictionary and sub-dicts.
#unable to appropriately call up the values, so I will just ignore some of the k:vs I wanted to include.
#	V9->11: nothing really, just migrated which server this script will run on. transitioned from
#centos to debian. moving on with v11 will try to just print out the dict that is returned from
#shodan, so it can be handled by logstash and placed into my elasticsearch DB.
#	v 1.1 -> 1.2: changing the script so that each shodan query's dict can be returned appropriately
#as a product of the query_shodan() function for further logic.
#	v 1.2 -> 1.5: basically introduce conditional logic and the ability pass shodan query dict into logstash.
#removed all the debugging catches present in v1.4.
#	v 1.5 -> 1.7: Verified that the socket module is working as intended and can handle what I make it do. Added exception
#handling and confirmed desired funcitonality while using the full IP list.
