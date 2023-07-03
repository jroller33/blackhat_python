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



for mac_addr in getmac_output:                 # loop thru output
    
    mac_find = mac_addr_regex.search(mac_addr)  # use regex to find mac addresses

    transport_find = transport_name.search(mac_addr)    # use regex to find transport name

    if mac_find == None or transport_find == None:      # if one of them isn't found, option won't be listed
        continue

    mac_addresses.append((mac_find.group(0), transport_find.group(0)))  # append a tuple with mac addr and transport name to list


# menu to choose mac addr
print("Which MAC address do you want to update?")
for index, item in enumerate(mac_addresses):
    print(f"{index} - MAC address: {item[0]} - Transport Name: {item[1]}")

# user selects the mac addr they want to change 
user_option = input("Select a menu number for the MAC address you want to change:")

# menu so the user can pick a new mac addr
while True:
    print("Which MAC address do you want to use? This changes the network card's MAC address")
    for index, item in enumerate(new_mac_addr):
        print(f"{index} = MAC address: {item}")

        # user selects their new mac addr
        update_option = input("Select the menu number for your new MAC address:")


        # validate user input
        if int(update_option) >= 0 and int(update_option) < len(new_mac_addr):
            print(f"Your MAC address will be changed to: {new_mac_addr[int(update_option)]}")
            break
        else:
            print("Invalid selection. Try again")

