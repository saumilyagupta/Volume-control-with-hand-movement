import cv2 as cv
import cv2
import mediapipe as mp
import time
import numpy as np
import handtraking_module as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# volume.SetMasterVolumeLevel(-20.0, None)

####################
wCam, hCam = 640,480
vMin, vMax, _=volume.GetVolumeRange()
lenMax = 200
lenMin = 55
vol =0
volBar = 400
volper=0
####################

detector = htm.handDetector(detectionCon=0.7)

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime =0
while True:

    sucess , img = cap.read()
    img =detector.findHands(img)
    list1=detector.findPosition(img,draw=False)
    if len(list1)!=0:
        # print(list1[8],list1[4])
        cv.line(img,(list1[4][1],list1[4][2]),(list1[8][1],list1[8][2]),(22,45,56),2)
        cv.circle(img,(list1[4][1],list1[4][2]),15,(222,22,222),cv.FILLED)
        cv.circle(img,(list1[8][1],list1[8][2]),15,(222,22,222),cv.FILLED)
        cv.circle(img,((list1[8][1]+list1[4][1])//2,(list1[8][2]+list1[4][2])//2),13,(222,22,222),cv.FILLED)

        lenght = math.hypot((list1[8][1]-list1[4][1]),(list1[8][2]-list1[4][2]))
        print(lenght)

        vol = np.interp(lenght, [lenMin,lenMax],[vMin,vMax])
        volBar= np.interp(lenght,[lenMin,lenMax],[400,150])
        volper= np.interp(lenght,[lenMin,lenMax],[0,100]) 
        if lenght<60:
            cv.circle(img,((list1[8][1]+list1[4][1])//2,(list1[8][2]+list1[4][2])//2),13,(0,0,222),cv.FILLED)
        if lenght<=300:  
            volume.SetMasterVolumeLevel(vol, None)
    cv.putText(img,f"VOL:{int(volper)}%",(12,140),cv.FONT_HERSHEY_PLAIN,2,(255, 0, 255),2)            
    cv.rectangle(img , (15, 150), (40,400),(255,255,0),2)
    cv.rectangle(img , (17, int(volBar)+1), (37,400-1),(255, 0, 255),cv.FILLED)
            


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime 
    cv.putText(img, f"FPS:{int(fps)}  ", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
    cv.imshow("video", img)
    cv.waitKey(1)