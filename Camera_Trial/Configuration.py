import sys
import os
import platform
import requests
import traceback

_OPERATING_SYSTEM = 0
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = 0

#This method allows the user to input the settings, Then registers the device with API
def settingsWriter():
    global _SETTINGS_FILE
    try:
        print(r"(Include '/' at the end of URLs and '/' or '\\' to File Paths depending on OS!)")
        domain = input("Enter the API URL/IP Address: ")
        _SETTINGS_FILE.write("Domain; " + domain + "\n")
        ImagePath = input("Enter the Path to a folder to save Captured Images: ")
        _SETTINGS_FILE.write("ImagePath; " + ImagePath + "\n")
        Octoprint = input("Enter the Domain/IP Address of the Raspberry Pi running OctoPrint: ")
        _SETTINGS_FILE.write("OctoPiAddress; " + Octoprint + "\n")
        Octoprint_API = input("Enter the Octoprint API Key: ")
        _SETTINGS_FILE.write("OctoPiKey; " + Octoprint_API + "\n")
        Arduino_Baudrate = input("Enter the Arduino Baudrate: ")
        _SETTINGS_FILE.write("ArduinoBaudrate; " + Arduino_Baudrate + "\n")
        ImageCaptureInterval = input("Enter how often to take a picture (In Seconds!): ")
        _SETTINGS_FILE.write("ImageInterval; " + ImageCaptureInterval + "\n")
        PrinterPollInterval = input("Enter how often to Poll the printer (In Seconds!): ")
        _SETTINGS_FILE.write("PollInterval; " + PrinterPollInterval + "\n") 
        ArduinoInactivityLength = input("Enter how long the Arduino can be inactive for (In Seconds!): ")
        _SETTINGS_FILE.write("ArduinoInactivityLength; " + ArduinoInactivityLength + "\n") 
        deviceName = platform.uname()[1]
        _SETTINGS_FILE.write("DeviceName; " + deviceName + "\n")

        #Appends the web method name to the end of the  
        RegAPI = domain + "api/DeviceRegistration/Register"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        files = 'DevName=' + deviceName
        resp = requests.request("POST", RegAPI, headers=headers, data = files)
        UUID = resp.text
        _SETTINGS_FILE.write("DeviceUUID; " + UUID + "\n")
        print("File Successfully written!")
        input("Press Enter to Exit Program...")
    except:
        print("A problem was encountered, printing stacktrace")
        traceback.print_last()
    finally:
        _SETTINGS_FILE.close()


    
# Method lets the user confirm the current settings available if the file exist, otherwise jumps to the editing method.
def editFile(exists):
    if exists == True:
        global _SETTINGS_FILE
        lines = _SETTINGS_FILE.readlines()
        for x in lines:
            print(x)
        choice = input("Are these settings okay? (Yes or No)")
        choice = choice.upper()
        if choice == "YES":
            _SETTINGS_FILE.close()
            try:
                sys.exit(0)
            except:
                print("Exiting")
        elif choice == "NO":
            _SETTINGS_FILE.close()
            _SETTINGS_FILE = open(_SETTING_FILE_PATH, "w")
            settingsWriter()
            print("Exiting")

    else:
        settingsWriter()


#Checks the Current OS for compatability, Would likely work on Mac however Linux will most likely be used.
if sys.platform.startswith('linux'):
    _OPERATING_SYSTEM = 1
elif sys.platform.startswith('win32'):
    _OPERATING_SYSTEM = 2
else:
    print("Compatible OS's: Linux And windows. \nIf you're seeing this message then your OS isn't compatible")
    input("Press enter to continue...")

# Within A Try Catch due to Sys.Exit throwing an exiting rxception when called to warn the system.
try:
    if _OPERATING_SYSTEM != 0:

        #Gets the Current location of the script, Purely Informational
        path = os.getcwd()
        print ("The current working directory is %s" % path)

        #Sets the Setup File Location based on which OS is Detected 
        if _OPERATING_SYSTEM == 1:
            _SETTING_FILE_PATH = "~/Camera_Script_Setup/"
        elif _OPERATING_SYSTEM == 2:
            _SETTING_FILE_PATH = "C:\\Camera_Script_Setup\\"
    
        #Checks to see if the Directory for the Camera setup script exists.
        if os.path.exists(_SETTING_FILE_PATH):
            _SETTING_FILE_PATH += "setup.ini"

            #Checks to see if the file exists within the directory. Then allows the User to choose to change settings or exit.
            if os.path.exists(_SETTING_FILE_PATH):
                choice = input("Would you like to change the settings? ('Yes' or 'No')")
                choice = choice.upper()
                if choice == "YES":
                    _SETTINGS_FILE = open(_SETTING_FILE_PATH, "r+")
                    editFile(True)
                else:
                    sys.exit(0)
            else:
                _SETTINGS_FILE = open(_SETTING_FILE_PATH, "w+")
                editFile(False)
        else:
            #Creates and then opens the settings files for editing
            os.mkdir(_SETTING_FILE_PATH)
            _SETTING_FILE_PATH += "setup.ini"
            _SETTINGS_FILE = open(_SETTING_FILE_PATH, "w+")
            editFile(False)
    else:
        sys.exit(0)
except:
    print("Exiting...")
                    

