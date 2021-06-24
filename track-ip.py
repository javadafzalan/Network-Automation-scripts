from netmiko import Netmiko
import re
import getpass
import os
from datetime import datetime
import re
import creds

def validate_ip(ip):    
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if(re.search(regex,ip)):
        return True
    else:
        return False
def get_host_info(ip,username,password):
    import wmi
    HOSTNAME=""
    OS=""
    try:
        
        conn = wmi.WMI(ip, user=username, password=password)
        for item in conn.Win32_OperatingSystem():
            OS=item.Caption
            HOSTNAME=item.CSName
        return HOSTNAME,OS
    except:
        return HOSTNAME,OS

print("----------------------------------------------------------------------------------------------------------------------------------")
print("                                     .:   Host tracker   :.")
print("----------------------------------------------------------------------------------------------------------------------------------")
print("                                   .:Enter Device Credentials:. ")
CURRENT_PATH=os.path.dirname(os.path.abspath(__file__))
FINAL_OUTPUT=""
#USERNAME=input("Devices username : ")
#PASSWORD=getpass.getpass("Devices Password : ")
#ENABLE=getpass.getpass("Devices Enable Password : ")
#AD_USERNAME=input("Active Directory Username : ")
#AD_PASSWORD=getpass.getpass("Active Directory Password : ")
#credentials is in a gitignore file
USERNAME=creds.USERNAME
PASSWORD=creds.PASSWORD
ENABLE=creds.ENABLE
AD_USERNAME=creds.AD_USERNAME
AD_PASSWORD=creds.AD_PASSWORD
LOOKING_HOST=input("for which device you'r looking for ? : ")

IPDT_LIST=[]
IPDT_DICT={}
#list of campus lan switches should be in device-list.txt
file1=open(CURRENT_PATH + "\\device-list.txt")
print("Reading list of devices from: "+CURRENT_PATH+"\\device-list.txt")
DEVICE_LIST=file1.readlines()
file1.close()
DEVICE_ERR_LIST=[]
print("--------------------------------------------------")
LIST_OF_DATA=[]
start_time = datetime.now()
print("Start time : " + str(start_time))
for device in DEVICE_LIST:
    device=device.strip("\n")
    DEVICE_DICT = {
    "host": device,
    "username": USERNAME,
    "password": PASSWORD,
    "secret" : ENABLE,
    "device_type": "cisco_ios"}
    print("Connecting to device : "+ device)
    #try:
    net_connect = Netmiko(**DEVICE_DICT)
    net_connect.enable()
    output=net_connect.send_command("show ip device tracking all")    
    output_row=output.splitlines()
    #evaluate every row to find ip addresses
    for row in output_row:
        if(row!=""):
            if(validate_ip(row.split()[0])):
                IPDT_LIST.append([device,row.split()[0],row.split()[1],row.split()[2],row.split()[3],row.split()[4]])
                IPDT_DICT[row.split()[0]]={"switch" : device, "mac" : row.split()[1], "vlan" : row.split()[2], "interface" : row.split()[3] , "state" : row.split()[4]}
    print("host list gathered.")
    print("---------------------------------------")
    net_connect.disconnect()
    #except:
    #print("error on device : "+ device)
    #DEVICE_ERR_LIST.append(device)

print("*********************************************")
HOST_DICT=IPDT_DICT[LOOKING_HOST]
hostinfo=get_host_info(LOOKING_HOST,AD_USERNAME,AD_PASSWORD)
print("host {} is connected to switch {},on port {} and placed in vlan {}".format(LOOKING_HOST,HOST_DICT['switch'],HOST_DICT['interface'],HOST_DICT['vlan']))
print("hostname : {}, Os : {} ".format(hostinfo[0],hostinfo[1]))
print("*********************************************")
end_time = datetime.now()
print("Total time is : "+str(end_time - start_time))
