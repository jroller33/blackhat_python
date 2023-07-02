import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime

# all active wifi networks are saved in this list
active_wireless_networks = []

# checks if ESSID is already in the list. If not, it gets added to active_wireless_networks
def check_for_essid(essid, list):
    check_status = True

    if len(list) == 0:
        return check_status
    
    for item in list:
        if essid in item["ESSID"]:
            check_status = False

    return check_status