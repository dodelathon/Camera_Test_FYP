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

RegAPI = "https://donal-doherty.com/api/DeviceData/GetStats"
headers = {'Device': '006e6589-1cd7-410d-912c-f2588541a1e3'}
resp = requests.get(RegAPI, headers = headers)
#resp = requests.request("GET", RegAPI, headers=headers)
UUID = resp.text
dict = json.loads(UUID)
print("Printing recieved text")
print(UUID)
jsonFile = open("Stats.json", "w+")
temp = ""
for x in dict:
    print(x)
    temp += x
jsonFile.write(temp)
jsonFile.seek(0)
lines = jsonFile.read().split('\n')
print()
print("Printing file text")
print()
for x in lines:
    print(x)
    print("\n")
jsonFile.seek(0)
bob = json.load(jsonFile)
for x in bob:
    print(x)



#dict = json.loads(UUID)
#print("\nNow printing the dictionary\n")
#bob = ""

#bob = json.loads(temp)
#print("\n")
#for x in bob:
#    print(x)
#    for y in bob[x]:
#        print("     " + y)
#    print("\n")

