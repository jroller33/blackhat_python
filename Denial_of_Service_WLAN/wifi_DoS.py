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