from netmiko import Netmiko
import re
import getpass
import os
from datetime import datetime
def GET_HOSTNAME(showrun):
    left = 'hostname '
    right = ' '
    leftstr=showrun[showrun.index(left):]
    end_len=leftstr[9:].index("\n")
    return(leftstr[9: 9+ end_len])

print("----------------------------------------------------------------------------------------------------------------------------------")
print("                                     .:  Cisco IOS Info Grabber   :.")
print("----------------------------------------------------------------------------------------------------------------------------------")
#print("                                                 .:Enter Device Credentials:. ")
CURRENT_PATH=os.path.dirname(os.path.abspath(__file__))
FINAL_OUTPUT=""
USERNAME=input("Enter device username : ")
PASSWORD=getpass.getpass("Enter device password : ")
ENABLE=getpass.getpass("Enter device enable secret : ")
file1=open(CURRENT_PATH + "\\device-list.txt")
print("Reading list of devices from: "+CURRENT_PATH+"\\device-list.txt")
DEVICE_LIST=file1.readlines()
file1.close()
DONE_DEVICES=0
FAILED_DEVICE=0
TOTAL_DEVICES=len(DEVICE_LIST)
DEVICE_ERR_LIST=[]
file2=open(CURRENT_PATH + "\\command-list.txt")
config_commands=file2.readlines()
file2.close()
print("--------------------------------------------------")
LIST_OF_DATA=[]
SHOW_RUN=""
start_time = datetime.now()
print("Start time : " + str(start_time))
for device in DEVICE_LIST:
    SHOW_CONTENT=""
    DEVICE_DICT = {
    "host": device,
    "username": USERNAME,
    "password": PASSWORD,
    "secret" : ENABLE,
    "device_type": "cisco_ios"}
    print("Connecting to device "+ str(DONE_DEVICES) +" : "+ device)
    try:
        net_connect = Netmiko(**DEVICE_DICT)
        net_connect.enable()
        SHOW_RUN=net_connect.send_command("show runn")
        hostname=GET_HOSTNAME(SHOW_RUN)
        HOSTDIR=CURRENT_PATH + "\\"+hostname
        os.mkdir(HOSTDIR)
        for command in config_commands:
            command_output=net_connect.send_command(command)
            FILE_COMMAND=open(CURRENT_PATH +  "\\"+ hostname + "\\"+ hostname + "-"+ command.rstrip("\n") + ".txt","w")
            FILE_COMMAND.write(command_output)
            FILE_COMMAND.close()
        print(hostname)
        FILE_SHOWRUN=open(CURRENT_PATH +  "\\"+ hostname + "\\"+ hostname + "-" + "show running-config" + ".txt","w")
        FILE_SHOWRUN.write(SHOW_RUN)
        FILE_SHOWRUN.close()
        print("Switch " + device + " is done.")
        print("---------------------------------------")    
        print("Remaining devices : "+ str(TOTAL_DEVICES - DONE_DEVICES - FAILED_DEVICE))
        net_connect.disconnect()
        DONE_DEVICES+=1
    except:
        print("error on device : "+ device)
        DEVICE_ERR_LIST.append(device)
        FAILED_DEVICE+=1
end_time = datetime.now()

print("Total time is : "+str(end_time - start_time))
print("Device with Error in this Configuration : ")

for item in DEVICE_ERR_LIST:
    print("ERROR Device IP : "+item)