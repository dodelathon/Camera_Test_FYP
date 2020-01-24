import math
import cv2
import requests
import sys
import os

_OPERATING_SYSTEM = 0
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = 0
_ATTRIBUTE_LIST = {}

if sys.platform.startswith('linux'):
    _OPERATING_SYSTEM = 1
elif sys.platform.startswith('win32'):
    _OPERATING_SYSTEM = 2
else:
    print("Compatible OS's: Linux And windows. \nIf you're seeing this message then your OS isn't compatible")
    input("Press enter to continue...")
    sys.exit()

if _OPERATING_SYSTEM == 1:
     _SETTING_FILE_PATH = "~/Camera_Script_Setup/"
elif _OPERATING_SYSTEM == 2:
     _SETTING_FILE_PATH = "C:\\Camera_Script_Setup\\"

if os.path.exists(_SETTING_FILE_PATH):
        _SETTING_FILE_PATH += "setup.ini"
        if os.path.exists(_SETTING_FILE_PATH):
            lines = open(_SETTING_FILE_PATH)
            for x in lines:
                kv = x.split(": ")
                _ATTRIBUTE_LIST[kv[0]] = kv[1]
    

url = "https://donal-doherty.com/api/image/Upload"
cap = cv2.VideoCapture(0)
x=1
counter = 0
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if(counter == 150):
        filename = 'D:\\Desktop\\cam_folder\\image.jpg'
        x += 1
        cv2.imwrite(filename, frame)
        files = {'photo' : ('image.jpg', open(filename, 'rb')), '_DeviceName': }
        r = requests.post(url, files=files)
        print(r.text)
        counter = 0
    counter += 1

cap.release()
print ("Done!")

