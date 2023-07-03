#!/usr/bin/env python3

# *** must be run with admin privileges, and wifi adapter must be connected to a network ***


import winreg       # Windows Registry access
import subprocess   # used to run sys commands as a child process of the parent process
import re           # regex
import codecs       # standard python encoders and decoders


# MAC addresses you want to try to use go here. When the script runs you'll choose one. Must be 12 valid hexadecimal values
# if it fails, change 2nd char to 2, 6, A or E. The ones in the list already should work:
new_mac_addr = ["0A1122334455", "OE1122334455", "021122334455", "061122334455"]

# empty list to store all MAC addresses
mac_addresses = list()

# regex for for MAC addresses
mac_addr_regex = re.compile(r"([A-Za-z0-9]{2}[:-]){5}([A-Za-z0-9]{2})")

# regex for transport names. This works for now, but be careful using .+ or .*
transport_name = re.compile("({.+})")

# regex to get adapter index
adapter_index = re.compile("([0-9]+)")


'''
subprocess.run(<command line arguments>)
output is stored in 'stdout' in bytes. decode it to unicode before using it as a string
run 'getmac' command and capture output. split the output so you can work with each line
'''
getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode().split('\n')


# loop thru output
for mac_addr in getmac_output:
    
    mac_find = mac_addr_regex.search(mac_addr)