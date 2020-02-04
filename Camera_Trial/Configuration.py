import sys
import os
import platform
import requests
import traceback

_OPERATING_SYSTEM = 0
_SETTING_FILE_PATH = ""
_SETTINGS_FILE = 0

def settingsWriter():
    global _SETTINGS_FILE
    try:
        domain = input("Enter the API URL/IP Address (Include '/' at the end): ")
        _SETTINGS_FILE.write("Domain; " + domain + "\n")
        ImagePath = input("Enter the Path to a folder to save Captured Images: ")
        _SETTINGS_FILE.write("ImagePath; " + ImagePath + "\n")
        deviceName = platform.uname()[1]
        _SETTINGS_FILE.write("DeviceName; " + deviceName + "\n")
        RegAPI = domain + "api/DeviceRegistration/Register"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        files = 'DevName=' + deviceName
        resp = requests.request("POST", RegAPI, headers=headers, data = files)
        UUID = resp.text
        print(UUID)
        _SETTINGS_FILE.write("DeviceUUID; " + UUID + "\n")
        print("File Successfully written!")
        input("Press Enter to Exit Program...")
    except:
        print("A problem was encountered, printing stacktrace")
        traceback.print_last()
    finally:
        _SETTINGS_FILE.close()


    

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
            sys.exit(1)
        elif choice == "NO":
            _SETTINGS_FILE.close()
            _SETTINGS_FILE = open(_SETTING_FILE_PATH, "w")
            settingsWriter()
            print("Exiting")

    else:
        settingsWriter()



if sys.platform.startswith('linux'):
    _OPERATING_SYSTEM = 1
elif sys.platform.startswith('win32'):
    _OPERATING_SYSTEM = 2
else:
    print("Compatible OS's: Linux And windows. \nIf you're seeing this message then your OS isn't compatible")
    input("Press enter to continue...")


if _OPERATING_SYSTEM != 0:
    path = os.getcwd()
    print ("The current working directory is %s" % path)
    if _OPERATING_SYSTEM == 1:
        _SETTING_FILE_PATH = "~/Camera_Script_Setup/"
    elif _OPERATING_SYSTEM == 2:
        _SETTING_FILE_PATH = "C:\\Camera_Script_Setup\\"
    
    if os.path.exists(_SETTING_FILE_PATH):
        _SETTING_FILE_PATH += "setup.ini"
        if os.path.exists(_SETTING_FILE_PATH):
            choice = input("Would you like to change the settings? ('Yes' or 'No')")
            choice = choice.upper()
            if choice == "YES":
                _SETTINGS_FILE = open(_SETTING_FILE_PATH, "r+")
                editFile(True)
            else:
                sys.exit(1)
        else:
            _SETTINGS_FILE = open(_SETTING_FILE_PATH, "w+")
            editFile(False)
    else:
        os.mkdir(_SETTING_FILE_PATH)
        _SETTING_FILE_PATH += "setup.ini"
        _SETTINGS_FILE = open(_SETTING_FILE_PATH, "w+")
        editFile(False)
else:
    sys.exit(1)
                    

