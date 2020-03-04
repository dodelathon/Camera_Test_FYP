import math
import cv2
import requests
import sys
import io
import os
import serial
import serial.tools.list_ports


_OPERATING_SYSTEM = 0
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = 0
_ATTRIBUTE_LIST = {}
_ARDUINO = 0
_S_PORT = 0

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
     _SETTING_FILE_PATH = "~/Camera_Script_Setup/"
elif _OPERATING_SYSTEM == 2:
     _SETTING_FILE_PATH = "C:\\Camera_Script_Setup\\"

if os.path.exists(_SETTING_FILE_PATH):
        _SETTING_FILE_PATH += "setup.ini"
        if os.path.exists(_SETTING_FILE_PATH):
            lines = open(_SETTING_FILE_PATH).read().split('\n')
            for x in lines:
                if x != "":
                    kv = x.split("; ")
                    _ATTRIBUTE_LIST[kv[0]] = kv[1]
                    print(kv[0] + " : " + kv[1])
     
RegAPI = _ATTRIBUTE_LIST['OctoPiAddress'] + "api/printer"
print(RegAPI)
print(_ATTRIBUTE_LIST['OctoPiKey'])
headers = {'X-Api-Key':_ATTRIBUTE_LIST['OctoPiKey']}
resp = requests.request("GET", RegAPI, headers=headers)
print(resp.text)