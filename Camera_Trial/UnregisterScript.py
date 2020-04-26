#Imports
import math
import requests
import sys
import io
import serial
import serial.tools.list_ports
import os
import timeit
import json
import time
from pathlib import Path

#Initialization of Global Variables
_OPERATING_SYSTEM = None
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = None
_ATTRIBUTE_LIST = {}



#Determines the platform the Code is running on. 
if sys.platform.startswith('linux'):
    _OPERATING_SYSTEM = 1
elif sys.platform.startswith('win32'):
    _OPERATING_SYSTEM = 2
else:
    print("Compatible OS's: Linux And windows. \nIf you're seeing this message then your OS isn't compatible")
    input("Press enter to continue...")
    try:
        sys.exit(1)
    except:
        print("Exiting...")

if _OPERATING_SYSTEM == 1:
     _SETTING_FILE_PATH = str(Path.home()) + "/Camera_Script_Setup/"
elif _OPERATING_SYSTEM == 2:
     _SETTING_FILE_PATH = "C:\\Camera_Script_Setup\\"

#Open the configuration and then reads in the settings.
if os.path.exists(_SETTING_FILE_PATH):
        _SETTING_FILE_PATH += "setup.ini"
        if os.path.exists(_SETTING_FILE_PATH):
            lines = open(_SETTING_FILE_PATH).read().split('\n')
            for x in lines:
                if x != "":
                    kv = x.split("; ")
                    _ATTRIBUTE_LIST[kv[0]] = kv[1]
                    print(kv[0] + " : " + kv[1])

RegAPI = _ATTRIBUTE_LIST["Domain"] + "api/DeviceRegistration/RemoveDevice"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
files = 'UUID=' + _ATTRIBUTE_LIST["DeviceUUID"]
resp = requests.request("POST", RegAPI, headers=headers, data = files)
print(resp.text)

choice = input("Would you like to Delete configuation file(Y or N)?")
if choice.upper() == "Y":
    if os.path.exists(_SETTING_FILE_PATH):
        os.remove(_SETTING_FILE_PATH)
        print("File Deleted")
else:
    print("Exiting...")