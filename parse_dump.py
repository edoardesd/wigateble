#!/usr/bin/python
import sys
import itertools
import pprint as pp

client_list = {}
FILE_PATH = sys.argv[1]


'''
	remove LAP in vendor
	remove milliseconds in ts
'''
def remove_unused_substring():
	for key, val in client_list.items():
		val["vendor"] = val["vendor"][:-9]
		if ":" in val["vendor"]:
			val["vendor"] = "unknown"
		val["closest_ts"] = val["closest_ts"][:-15]

'''
	create the dictionary of the client
	one key for each unique mac address
'''
def load_dict(big_list):
	for probe in big_list:
		probe = probe.split('|') 	#create the list of single probe
		ts, mac_resolved, mac_addr, rssi, ssid = probe #unpack the list
		
		if not client_list.has_key(mac_addr):
				client_list[mac_addr] = {"closest_ts": ts, "times_seen": 1, "closest_rssi": rssi, "vendor": mac_resolved, "ssid": [ssid]}
		else:
			client_list[mac_addr]["times_seen"] += 1 
			if rssi <= client_list[mac_addr]["closest_rssi"]:
				client_list[mac_addr]["closest_rssi"] = rssi
				client_list[mac_addr]["closest_ts"] = ts
				if ssid not in client_list[mac_addr]["ssid"]:
					client_list[mac_addr]["ssid"].append(ssid)
					client_list[mac_addr]["ssid"] = filter(None, client_list[mac_addr]["ssid"]) #delete last field if it's empty (no ssid inside probe)


if __name__ == '__main__':
	print "loading from ", FILE_PATH
	lines = [line.rstrip('\n') for line in open(FILE_PATH)] #load the file

	load_dict(lines) #manipulate the data // fill the dict
	remove_unused_substring()

	pp.pprint(client_list)
