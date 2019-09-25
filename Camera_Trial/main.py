import math
import cv2
import requests

url = "https://donal-doherty.com/api/image"
cap = cv2.VideoCapture(0)
x=1
counter = 0
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if(counter == 30):
        filename = 'D:\\Desktop\\cam_folder\\image.jpg'
        x += 1
        cv2.imwrite(filename, frame)
        files = {'photo' : ('image.jpg', open(filename, 'rb'))}
        r = requests.post(url, files=files)
        print(r.text)
        counter = 0
    counter += 1

cap.release()
print ("Done!")

