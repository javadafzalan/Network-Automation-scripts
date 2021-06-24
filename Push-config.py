from netmiko import Netmiko
import re
import getpass
import os
from datetime import datetime
import creds
print("----------------------------------------------------------------------------------------------------------------------------------")
print("                                     .:   Cisco Router Switch Device Mass Config Pusher   :.")
print("----------------------------------------------------------------------------------------------------------------------------------")
print("                                                 .:Enter Device Credentials:. ")
CURRENT_PATH=os.path.dirname(os.path.abspath(__file__))
FINAL_OUTPUT=""
USERNAME=input("Device username : ")
PASSWORD=getpass.getpass("Device Password : ")
ENABLE=getpass.getpass("Device Enable Password : ")
file1=open(CURRENT_PATH + "\\device-list.txt")
print("Reading list of devices from: "+CURRENT_PATH+"\\device-list.txt")
DEVICE_LIST=file1.readlines()
file1.close()
DEVICE_ERR_LIST=[]
file2=open(CURRENT_PATH + "\\config-list.txt")
config_commands=file2.readlines()
print("--------------------------------------------------")
file2.close()
LIST_OF_DATA=[]
start_time = datetime.now()
print("Start time : " + str(start_time))
for device in DEVICE_LIST:
    DEVICE_DICT = {
    "host": device,
    "username": USERNAME,
    "password": PASSWORD,
    "secret" : ENABLE,
    "device_type": "cisco_ios"}
    print("Connecting to device : "+ device)
    try:
        net_connect = Netmiko(**DEVICE_DICT)
        #net_connect.enable()
        #print(net_connect.find_prompt())
        output=net_connect.send_config_set(config_commands)
        print(output)
        print("Switch " + device + " is done.")
        print("---------------------------------------")
        net_connect.save_config()
        net_connect.disconnect()
    except:
        print("error on device : "+ device)
        DEVICE_ERR_LIST.append(device)
end_time = datetime.now()
print("Total time is : "+str(end_time - start_time))
print("Device with Error in this Configuration : ")
for item in DEVICE_ERR_LIST:
    print("Device IP : "+item)