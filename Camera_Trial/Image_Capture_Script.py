import math
import cv2
import requests
import sys
import os
import time
from pathlib import Path

# Declaration of Global Variables

_OPERATING_SYSTEM = 0
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = 0
_ATTRIBUTE_LIST = {}
_API_PATH = "api/image/Upload"

# Checks the OS and sets the pathing string correctly for each system

if sys.platform.startswith('linux'):
    _OPERATING_SYSTEM = 1
elif sys.platform.startswith('win32'):
    _OPERATING_SYSTEM = 2

if _OPERATING_SYSTEM == 1 or _OPERATING_SYSTEM == 0 :
     _SETTING_FILE_PATH = str(Path.home()) + "/Camera_Script_Setup/"
elif _OPERATING_SYSTEM == 2:
     _SETTING_FILE_PATH = "C:\\Camera_Script_Setup\\"

# Checks to see if the Config file exists and then reads in the Setting into the program to be used.

if os.path.exists(_SETTING_FILE_PATH):
        _SETTING_FILE_PATH += "setup.ini"
        if os.path.exists(_SETTING_FILE_PATH):
            lines = open(_SETTING_FILE_PATH).read().split('\n')
            for x in lines:
                if x != "":
                    kv = x.split("; ")
                    _ATTRIBUTE_LIST[kv[0]] = kv[1]
                    print(kv[0] + " : " + kv[1])
else:
    try:
        print("Configuration File not found, Please run the configuration script and try again!")
        sys.exit(0)    
    except:
        print("")

# Sets the API upload URL, Utilizes OpenCV to connect to the camera and sends a frame every 5 seconds to the server.
url = _ATTRIBUTE_LIST["Domain"] + _API_PATH
cap = cv2.VideoCapture(0)
Interval = int(_ATTRIBUTE_LIST["ImageInterval"])
header = {'_Device':_ATTRIBUTE_LIST["DeviceUUID"]}

try:
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (ret != True):
            break

        time.sleep(Interval)
        filename = _ATTRIBUTE_LIST["ImagePath"] + "image.jpg"   
        filename = filename.strip()
        cv2.imwrite(filename, frame)
        file = {'photo' : ('image.jpg', open(filename, 'rb'))}
        r = requests.post(url, files=file, headers=header)
        print(r.status_code)
        print(r.text)
    cap.release()
except:
    cap.release()
    print("An error has occured during the capture process, closing...")

