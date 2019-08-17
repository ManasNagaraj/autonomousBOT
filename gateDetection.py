# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 12:38:44 2019

@author: Manas
"""

import cv2 
import numpy as np



cap = cv2.VideoCapture(0)


#this function will threshold the red colour and then give the array of contour
#lines
def gateDetectRedUpper(frame):
    cv2.imshow("t2",frame)
    lower_red = np.array([160,100,100]) 
    upper_red = np.array([185,255,255]) 
    imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    threshold = cv2.inRange(imgHSV,lower_red,upper_red)
    
    return threshold

##########################this function will detect the other part of red##############################
    
def gateDetectRedLower(frame):
    
    lower_red = np.array([0,100,100]) 
    upper_red = np.array([10,255,255]) 
    imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    threshold = cv2.inRange(imgHSV,lower_red,upper_red)
    
    return threshold    
    
#################this function will threshold green colour and then give the contour lines for further processing################

def gateDetectGreen(frame):
    lower_green = np.array([40,100,50]) 
    upper_green = np.array([80,255,255]) 
    imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    threshold = cv2.inRange(imgHSV,lower_green,upper_green)    
    
    return threshold
 
    
######################his function will find the contours##################################### 
def findContour(frame):
    canny_output= cv2.Canny(frame,100,200)  
    img,contours,hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    return contours 
    
    
def areaSort(contours):
    
    if len(contours) != 0:
        c = max(contours, key = cv2.contourArea)

        return c
    
def drawRect(contours,frame):
    
    x,y,w,h = cv2.boundingRect(contours)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,160,0),2)
    
    
    return frame,(x+(0.5*w),y+(0.5*h))



def calMidPt(centre_red,centre_green):
    centre_red = list(centre_red)
    centre_green = list(centre_green)
    centre_gate =[]
    centre_gate.append(centre_red[1]*0.5+centre_green[1]*0.5)
    centre_gate.append(centre_red[0]*0.5+centre_green[0]*0.5)
    #print(centre_gate)################print center coordinate by uncommenting###########
    return centre_gate
    
def direction(centre_gate):
    destiny=""
    
    if(centre_gate[1]>325):
        destiny="right"
    
    elif(centre_gate[1]<315):
        destiny="left"
    else:
        destiny = "go straight boi"
    return destiny

    
    
while True:    
    __,frame = cap.read()
    blur = cv2.GaussianBlur(frame,(7,7),0)
    threshold_red_lower = gateDetectRedLower(blur)
    threshold_red_upper = gateDetectRedUpper(blur)
    threshold_green = gateDetectGreen(blur)
    
    threshold_red = cv2.add(threshold_red_upper,threshold_red_lower)
    
    cv2.imshow("green thresholding",threshold_red)
    cv2.imshow("red thresholding",threshold_green)
    
    contours_red = findContour(threshold_red)
    contours_green = findContour(threshold_green)
    
    contours_green_max = areaSort(contours_green)
    contours_red_max = areaSort(contours_red)
    
    
    frame1,center_red = drawRect(contours_red_max,frame)
    
    
    
    final_frame,center_green = drawRect(contours_green_max,frame1)
    centre_gate = calMidPt(center_red,center_green)
    destiny = direction(centre_gate)
    
    print(destiny)
    cv2.imshow("final frame",final_frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
    


