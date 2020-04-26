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
from datetime import datetime

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


#This portion detects connected serial devices and searches for an attached arduino     
ports = list(serial.tools.list_ports.comports())
for p in ports:
    if "Arduino" in p[1] or "ACM" in p[1]:
        _ARDUINO = p
        _FOUND = True
        print("Arduino Found, using the first!")

#If and arduino is found, a connection is initiated.
if _FOUND != False:
    _S_PORT = serial.serial_for_url(_ARDUINO[0], baudrate=_ATTRIBUTE_LIST['ArduinoBaudrate'], timeout=0)
    sio = io.TextIOWrapper(io.BufferedRWPair(_S_PORT, _S_PORT))
    Time = timeit.default_timer()
    ProblemTime = timeit.default_timer()

OctoAPI = _ATTRIBUTE_LIST["OctoPiAddress"]
OctoHeaders = {'X-Api-Key': _ATTRIBUTE_LIST["OctoPiKey"]}
StatsAPI = _ATTRIBUTE_LIST["Domain"] + "api/DeviceData/UpdateDeviceStats"
StatsHeaders = {"_Device": _ATTRIBUTE_LIST["DeviceUUID"]}
Interval = int(_ATTRIBUTE_LIST["PollInterval"])
Inactivity_Length = int(_ATTRIBUTE_LIST["ArduinoInactivityLength"])

#The main funtionality of this script is here. 
def main():
    stop = False
    while stop == False:

        #This section polls the Octoprint instance connected to the printer (Script will likely be on the same Raspberry PI)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        	
        resp = ""
        jsonFile = open("Stats.json", "w+")
        try:
            resp = requests.get(OctoAPI + "api/printer", headers = OctoHeaders)
            if(resp.status_code == 409):
                jsonFile.write("{ \"state\" : \"" + resp.text + "\",")
                jsonFile.write("\"LastUpdate\" : \"" + dt_string + "\"}")
            else:
                resp = json.loads(resp.text)
                #If the Arduino is detected, will test if any feed issues have been detected
                if _FOUND == True:
                    resp["state"]["flags"]["ArduinoFound"] = _FOUND
                    resp["state"]["flags"]["FeedError"] = _PROBLEM_DETECTED
                    resp["state"]["flags"]["LastUpdate"] = dt_string
                    stop = _PROBLEM_DETECTED
                    #Tells the printer to pause the job if the a problem is detected
                    if _PROBLEM_DETECTED == True:
                        try: 
                            action = {"command":"pause", "action":"pause"}
                            resp = requests.post(OctoAPI + "api/job", json=action, headers = OctoHeaders)
                        except:
                            resp["state"]["flags"]["Communication"] = "Error communicating with the printer"

                else:
                    resp["state"]["flags"]["ArduinoFound"] = _FOUND
                    resp["state"]["flags"]["Time"] = dt_string
                
                jsonFile.write(json.dumps(resp))
        
        except:
            #Pauses script if there's an issue communicating to Octoprint
            if jsonFile.closed() == False:
                jsonFile.write("{\"Status\" : \"There was an issue sending the request, Octoprint may be offline!\",")
                jsonFile.write("\"Time\" : \"" + dt_string + "\"}")
                jsonFile.close()
            print("There was an issue sending the request,\nOctoprint may be offline!")
            stop = True

        #Checks to see if there is an active job, this stops the script from pausing if theres no movement on the Arduino due to no active job 
        resp = requests.get(OctoAPI + "api/job", headers = OctoHeaders)    
        resp = json.loads(resp.text)
        if resp["job"]["estimatedPrintTime"] is not None:
            #This section only activates if an arduino is connected. It checks to see if the rotory encoder in the head has moved. If not, signals there's been a problem with the print
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
        
        #Attempts to send Stats file to the server.
        try:
            files = {'StatsFile' : ('Stats.json', open("Stats.json", 'rb'))}
            r = requests.post(StatsAPI, files=files, headers = StatsHeaders)
            print(r.status_code)
            print(r.text)
        except:
            print("There was an error updating the Statistics on the Server!\nIs it offline?")
        time.sleep(Interval)

main()

end = False
while end == False:
    arg = input("There appears to be an issue, Continue? (Y or N)")
    arg = arg.upper()
    if arg == "Y":
        _PROBLEM_DETECTED = False
        Time = timeit.default_timer()
        ProblemTime = timeit.default_timer()
        main()
    else:
        end = True