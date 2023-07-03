#!/usr/bin/env python3

'''
*** this script doesn't need Kali Linux. It's meant to be run on Windows 10, to change the machine's MAC address ***
*** it must be run with admin privileges on Win 10, and the wifi adapter must be connected to a network ***
'''

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

# this is the first part of the key. append the folders where you search for the values
controller_key_part = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"

# connect to HKEY_LOCAL_MACHINE registry. If 'None', connect to local machine's registry
with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
    # create a list for the 21 folders
    controller_key_folders = [("\\000" + str(item) if item < 10 else "\\00" + str(item)) for item in range(0, 21)]

    for key_folder in controller_key_folders:

        try:
            # specify the registry we connected to, the controller key (controller_key_part and folder(key) name made with list comprehension)
            with winreg.OpenKey(hkey, controller_key_part + key_folder, 0, winreg.KEY_ALL_ACCESS) as regkey:
                
                # look at values under each key and try to find "NetCfgInstanceId" with the same transport ID as the user selection
                try:
                    # values in registry start at 0. Continues until WindowsError, then it starts with the next folder until the correct key is found with the correct value
                    count = 0
                    while True:

                        # unpacks each winreg value into name value and type
                        name, value, type = winreg.EnumValue(regkey, count)

                        count = count + 1

                        # check if "NetCfgInstanceId" is equal to transport number for selected mac addr
                        if name == "NetCfgInstanceId" and value == mac_addresses[int(user_option)][1]:
                            new_mac_addr = mac_to_change_to[int(update_option)]
                            winreg.SetValueEx(regkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac_addr)
                            print("Matched transport number successfully")


                        # get adapter list and find index of the adapter to disable
                        break

                except WindowsError:
                    pass

        except:
            pass

# disable and enable wireless devices
run_disable_enable = input("Do you want to disable and reenable wireless devices? Type Y to continue:")

if run_disable_enable.lower() == 'y':
    run_last = True
else:
    run_last = False

while run_last:

    # get a list of all network adapters. HAVE TO IGNORE ERRORS. It doesn't like the format of the data from the command running
    network_adapters = subprocess.run(["wmic", "nic", "get", "name, index"], capture_output=True).stdout.decode('utf-8', errors="ignore").split('\r\r\n')

    for adapter in network_adapters:

        # get index for each adapter
        adapter_index_find = adapter_index.search(adapter.lstrip())

        # if there's an index and the adapter is wireless, disable and enable it
        if adapter_index_find and "Wireless" in adapter:
            disable = subprocess.run(["wmic", "path", "win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "enable"], capture_output=True)

            # if return code is 0, adapter was disabled successfully
            if (enable.returncode == 0):
                print(f"Enabled {adapter.lstrip()}")

            # enable network adapter again
            enable = subprocess.run(["wmic", "path", f"win32_networkadapter", "where", f"index={adapter_index_find.group(0)}", "call", "enable"], capture_output=True)

            if (enable.returncode == 0):
                print(f"Enabled {adapter.lstrip()}")

    getmac_output = subprocess.run("getmac", capture_output=True).stdout.decode()

    # recreate the mac addr as in getmac XX-XX-XX-XX-XX-XX from the 12 char string. split the string into 2 char long strings, then use "-".join(list) to recreate address
    mac_add = "-".join([(new_mac_addr[int(update_option)][i:i+2]) for i in range(0, len(new_mac_addr[int(update_option)]), 2)])

    if mac_add in getmac_output:
        print("MAC address success")

    break