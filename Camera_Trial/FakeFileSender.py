#Imports
import math
import cv2
import requests
import sys
import io
import serial
import serial.tools.list_ports
import os
import timeit
import json
import time

#Initialization of Global Variables
_OPERATING_SYSTEM = None
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = None
_ATTRIBUTE_LIST = {}
_ARDUINO = None
_S_PORT = None
_FOUND = False
_PROBLEM_DETECTED = False
Time = 0
ProblemTime = 0


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
     _SETTING_FILE_PATH = "~/Camera_Script_Setup/"
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

#This portion detects connected serial devices and searches for an attached arduino     
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "Arduino" in p[1]:
        _ARDUINO = p
        _FOUND = True
        print("Arduino Found, using the first!")

#If and arduino is found, a connection is initiated.
if _FOUND != False:
    _S_PORT = serial.serial_for_url(_ARDUINO[0], baudrate=_ATTRIBUTE_LIST['ArduinoBaudrate'], timeout=0)
    sio = io.TextIOWrapper(io.BufferedRWPair(_S_PORT, _S_PORT))
    Time = timeit.default_timer()
    ProblemTime = timeit.default_timer()

toggle = 0
StatsHeaders = {"_Device": _ATTRIBUTE_LIST["DeviceUUID"]}
url = _ATTRIBUTE_LIST["Domain"] + "api/DeviceData/UpdateDeviceStats"
Interval = int(_ATTRIBUTE_LIST["PollInterval"])
Inactivity_Length = int(_ATTRIBUTE_LIST["ArduinoInactivityLength"])
while True:
    files = ""
    if(toggle == 0):
        jsonFile = open("Stats1.json", "r+")
        lines = jsonFile.read().split('\n')
        hap = ""
        #print(lines)
        for x in lines:
            hap+=x
        jsonFile.close()
        os.remove("Stats1.json")
        
        jsonFile = open("Stats1.json", "w+")
        bob = json.loads(hap)
        bob["state"]["flags"]["Arduino"] = _FOUND
        bob["state"]["flags"]["FeedError"] = _PROBLEM_DETECTED
        bob = json.dumps(bob)
        jsonFile.write(bob);
        jsonFile.close()
        files = {'StatsFile' : ('Stats.json', open("Stats1.json", 'rb'))}
        toggle = 1
    else:
        jsonFile = open("Stats2.json", "r+")
        lines = jsonFile.read().split('\n')
        hap = ""
        #print(lines)
        for x in lines:
            hap+=x
        jsonFile.close()
        os.remove("Stats2.json")
        
        jsonFile = open("Stats2.json", "w+")
        bob = json.loads(hap)
        bob["state"]["flags"]["Arduino"] = _FOUND
        bob["state"]["flags"]["FeedError"] = _PROBLEM_DETECTED
        bob = json.dumps(bob)
        jsonFile.write(bob);
        jsonFile.close()
        files = {'StatsFile' : ('Stats.json', open("Stats2.json", 'rb'))}
        toggle = 0

    if _FOUND != False:
        sio.flush()
        input = sio.readline()
        ProblemTime = timeit.default_timer()
        if input != "" :
            Time = timeit.default_timer()
            _PROBLEM_DETECTED = False
            print(input)
            
        if(ProblemTime - Time) > Inactivity_Length and _PROBLEM_DETECTED == False:
            _PROBLEM_DETECTED = True
    
    r = requests.post(url, files=files, headers = StatsHeaders)
    UUID = r.text
    print(UUID)
    print(r.status_code)
    time.sleep(Interval)
