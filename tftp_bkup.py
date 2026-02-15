#remove () if you want to run this with ./    (#!/usr/bin/python3)
from netmiko import ConnectHandler
import os
import pwd
import grp
import time

# Add addresses here 👇👇
IP = ['192.168.122.1', '20.1.1.1']

# This function creates file with required permissions 👇👇
def filename (hostname):
    File = f"{hostname.lower()}-confg"

    with open (File, 'w') as f:
        f.write("")
    # Permission and ownership settings 👇👇
    os.chmod(File,0o766)
    
    #Change "tftp" if you are using other user group
    uid = pwd.getpwnam("tftp").pw_uid   #Coresponds to command 'id tftp' or 'id -u tftp'
    gid = grp.getgrnam("tftp").gr_gid   #Coresponds to command 'id tftp' or 'id -d tftp'
    os.chown(File, uid, gid)

# Device config 👇👇
count = 0
while True:
    for ip in IP:
        device = {
            'device_type': 'cisco_ios',
            'host': ip,
            'username': 'sam',
            'password': 'ccna',
            'secret': '1111'
        }
        # Device Connection stuff down here 👇👇
        print(f"Backup Iteration: {count}")
        connection = ConnectHandler(**device)
        connection.enable()

        # Hostname & File name 👇👇
        hostname = connection.send_command('sh run | sec hostname').strip('hostname ')
        filename(hostname)

        # Commandzzzzzz 👇👇
        command = connection.send_command_timing("copy running-config tftp:")
        command += connection.send_command_timing("192.168.122.38")
        command += connection.send_command_timing(f"{hostname.lower()}-confg")
        print(f"Backup completed for {hostname}")
        connection.disconnect()
        count += 1
        print('*'*23)
    time.sleep(10)
