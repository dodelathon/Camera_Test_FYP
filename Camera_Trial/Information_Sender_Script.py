#Imports
import math
import cv2
import requests
import sys
import io
import serial
import serial.tools.list_ports
import os
import timeit as time
import json

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
            lines.close()
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
    Time = time.default_timer()
    ProblemTime = time.default_timer()

OctoAPI = _ATTRIBUTE_LIST["OctoPiAddress"]
OctoHeaders = {'X-Api-Key': _ATTRIBUTE_LIST["OctoPiKey"]}
StatsAPI = _ATTRIBUTE_LIST["Domain"] + "api/DeviceData/UpdateDeviceStats"
StatsHeaders = {"Device": _ATTRIBUTE_LIST["DeviceUUID"]}

main()

end = False
while end == False:
    arg = input("There appears to be an issue, Continue? (Y or N)")
    arg = arg.upper()
    if arg == "Y":
        _PROBLEM_DETECTED = False
        Time = 0
        ProblemTime = 0
        main()
    else:
        end = True


#The main funtionality of this script is here. 
def main():
    stop = false
    while stop == false:

        #This section polls the Octoprint instance connected to the printer (Script will likely be on the same Raspberry PI)
        resp = ""
        jsonFile = open("Stats.json", "w+")
        try:
            resp = requests.get(OctoAPI + "api/job", headers = OctoHeaders)
            if(resp.status_code == 409):
                jsonFile.write("{ \"state\" : \"" + resp.text + "\"}")
            else:
                resp = json.loads(resp.text)
                if _FOUND == True:
                    resp["state"]["flags"]["ArduinoFound"] = _FOUND
                    resp["state"]["flags"]["FeedError"] = _PROBLEM_DETECTED
                    stop = True
                    try: 
                        action = {"command":"pause", "action":"pause"}
                        resp = requests.post(OctoAPI + "api/job", json=action, headers = OctoHeaders)
                        stop = True
                    except:
                        resp["state"]["flags"]["Communication"] = "Error communicating with the printer"

                else:
                    resp["state"]["flags"]["ArduinoFound"] = _FOUND
                
                jsonFile.write(json.dumps(resp))
        
        except:
            if jsonFile.closed() == False:
                jsonFile.write("{\"Status\" : \"There was an issue sending the request, Octoprint may be offline!\"}")
                jsonFile.close()
            print("There was an issue sending the request,\nOctoprint may be offline!")
            stop = True

        #This section only activates if an arduino is connected. It checks to see if the rotor in the head has moved. If not, signals there's been a problem with the print
        if _FOUND != False:
            sio.flush()
            input = sio.readline()
            ProblemTime = time.default_timer()
            if input != "" :
                Time = time.default_timer()
                _PROBLEM_DETECTED = False
                print(input)
            if(ProblemTime - Time) > 10 and _PROBLEM_DETECTED == False:
                _PROBLEM_DETECTED = True
        try:
            files = {'StatsFile' : ('Stats.json', open("Stats.json", 'rb')), '_Device': _ATTRIBUTE_LIST["DeviceUUID"]}
            r = requests.post(url, files=files)
        except:
            print("There was an error updating the Statistics on the Server!\nIs it offline?")
 



