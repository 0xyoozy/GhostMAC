import subprocess
import argparse
from os import geteuid
from re import search

def check_root():

    if geteuid() != 0:
        print("[-] Error: This script requires root privileges. Please run with sudo.")
        exit(1)

def change_mac(interface, new_mac):

    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])
        
def get_current_mac(interface):

    output = subprocess.check_output(["ifconfig", interface]).decode()
    mac_search = search(r"([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})", output)

    if mac_search:
        return mac_search.group(0)
    else:
        return "[-] Could not read MAC address!"
    
def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change it's MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    options = parser.parse_args()

    if not options.interface:
        print("[-] Please specify an interface, use --help for more info.")
        exit(1)
    elif not options.new_mac:
        print("[-] Please specify a mac address, use --help for more info.")
        exit(1)
    
    return options

if __name__ == "__main__":

    check_root()
    
    options = get_args()
    
    current_mac = get_current_mac(options.interface)
    print("\nCurrent MAC: " + str(current_mac) + "\n")
    
    change_mac(options.interface, options.new_mac)
    
    current_mac = get_current_mac(options.interface)
    
    if current_mac == options.new_mac:
        print("[+] MAC address was successfully changed.")
    else:
        print("[-] MAC address did not change.")