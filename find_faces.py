#!/usr/bin/python
from lib_setup import face_cascade, eye_cascade
import cv2
import os


cdir = os.getcwd()
#print(cdir)
#print(os.path.exists(cdir+"/images/people.jpg"))
img = cv2.imread(cdir+"/images/people.jpg")

#convert to gray
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#detect faces
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

#for each face
for (x,y,w,h) in faces:
    #draw rectangle around face
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    #select face as region of interest 
    roi_g = gray[y:y+h,x:x+h]
    roi_c = img[y:y+h,x:x+h]
    #within region of interest find eyes
    eyes = eye_cascade.detectMultiScale(roi_g)
    #for each eye
    for (ex,ey,ew,eh) in eyes:
        #draw retangle around eye
        cv2.rectangle(roi_c, (ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img) #shows image
cv2.waitKey(0) #waits until a key is pressed to progress
cv2.destroyAllWindows() #closes windows