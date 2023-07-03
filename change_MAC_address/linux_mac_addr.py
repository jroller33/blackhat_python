import subprocess
import string
import random
import re
import argparse


# THREE PARAMETERS TO RUN THIS SCRIPT:
# ------------------------------------
# 'interface': network interface name you want to change the MAC address (get it using 'ifconfig' or 'ip' commands in linux)

# '-r' or '--random': means you want your new MAC address to be random (don't use with -m)

# '-m' or '--mac': means you want to change to a specific mac address (don't use with -r)

# Example usage in a linux terminal: >>>$ python linux_mac_addr.py wlan0 -r
# this runs the script, changing the mac address of 'wlan0' to a new random mac address
# ------------------------------------


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


def change_mac_address(iface, new_mac_address):

    # disable network interface
    subprocess.check_output(f"ifconfig {iface} down", shell=True)

    # change the mac address
    subprocess.check_output(f"ifconfig {iface} hw ether {new_mac_address}", shell=True)

    # enable network interface again
    subprocess.check_output(f"ifconfig {iface} up", shell=True)


# main menu
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change Linux MAC address")
    parser.add_argument("interface", help="Network interface name on Linux")
    parser.add_argument("-r", "--random", action="store_true", help="Do you want to generate a random MAC address?")
    parser.add_argument("-m", "--mac", help="The new MAC address you want to change to")
    args = parser.parse_args()

    iface = args.interface
    if args.random:
        # if random parameter is set, generate a random MAC
        new_mac_address = get_random_mac_address()

    elif args.mac:
        # if specific mac addr is set, use it
        new_mac_address = args.mac

    # get the current MAC address
    old_mac_address = get_current_mac_address(iface)
    print("[*] Old MAC address:", old_mac_address)

    # change the MAC address
    change_mac_address(iface, new_mac_address)

    # check if it's really changed
    new_mac_address = get_current_mac_address(iface)
    print("[+] New MAC address:", new_mac_address)