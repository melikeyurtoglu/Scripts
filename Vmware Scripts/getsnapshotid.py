#!/usr/bin/python3

import sys,json

#print 'Number of arguments:', len(sys.argv), 'arguments.'

with open('$HOME/vmid', 'r') as file:
   json_data=json.load(file)

#print(sys.argv)
vmname=str(sys.argv[1]).strip("\n")
print(json_data[vmname])