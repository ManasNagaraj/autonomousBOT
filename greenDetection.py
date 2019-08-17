

import cv2
import numpy as np


cap = cv2.VideoCapture(0)

lower_green = np.array([40,100,100]) 
upper_green = np.array([80,255,255]) 


def drawRect(contours,frame):
    
    x,y,w,h = cv2.boundingRect(contours)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,160,0),2)
    
    
    return frame,(x+(0.5*w),y+(0.5*h))


def findContour(frame):
    canny_output= cv2.Canny(frame,100,200)  
    img,contours,hierarchy = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
 
    return contours 


def areaSort(contours):
    
    if len(contours) != 0:
        c = max(contours, key = cv2.contourArea)

        return c
    
     
while True:
    __,image = cap.read()
    
    imgHSV = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    threshold = cv2.inRange(imgHSV,lower_green,upper_green) 
    
    
    contours = findContour(threshold)
    
    max_contour = areaSort(contours)
    
    frame,pos = drawRect(max_contour,image)
    
    cv2.imshow("frame",frame)
    
    
    
    
    cv2.imshow("threshold",threshold)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
    
cv2.destroyAllWindows()
