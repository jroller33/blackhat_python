import subprocess
import string
import random
import re

# you can either change to a random mac addr, or a specific one

def get_random_mac_address():
    
    # get the uppercase hexdigits
    uppercase_hexdigits = ''.join(set(string.hexdigits.upper()))
    
    # 2nd character must be 0, 2, 4, 6, 8, A, C, or E
    mac_addr = ""
    for i in range(6):
        for j in range(2):
            if i == 0:
                mac_addr += random.choice("02468ACE")
            else:
                mac_addr += random.choice(uppercase_hexdigits)
        mac_addr += ":"
    return mac_addr.strip(":")

def get_current_mac_address(iface):
    # use the ifconfig command to get interface details, including mac addr
    # check_output() runs the command and returns the output
    output = subprocess.check_output(f"ifconfig {iface}", shell=True).decode()

    # mac addr is located after "ether". re.search() grabs it
    return re.search("ether (.+) ", output).group().split()[1].strip()

