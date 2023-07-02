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