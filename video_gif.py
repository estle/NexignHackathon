import os, cv2
import numpy as np 

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_eye.xml')

cdir = os.getcwd()

gif = cv2.VideoCapture(dir+"/gif/giphy.gif")
flag, mask = cap.read()

original_mask_h,original_mask_w,mask_channels = mask.shape

mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

ret, original_mask = cv2.threshold(mask_gray, 10, 255, cv2.THRESH_BINARY_INV)
original_mask_inv = cv2.bitwise_not(original_mask)

cap = cv2.VideoCapture(cdir+"/images/blogger.mp4")
ret, img = cap.read()
img_h, img_w = img.shape[:2]

while True:
    
    ret, img = cap.read()
    if ret==False: break
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        #retangle for testing purposes
        #img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        #coordinates of face region
        face_w = w
        face_h = h
        face_x1 = x
        face_x2 = face_x1 + face_w
        face_y1 = y
        face_y2 = face_y1 + face_h

        #mask size in relation to face by scaling
        mask_width = int(1.5 * face_w)
        mask_height = int(mask_width * original_mask_h / original_mask_w)
        
        #setting location of coordinates of mask
        mask_x1 = face_x2 - int(face_w/2) - int(mask_width/2)
        mask_x2 = mask_x1 + mask_width
        mask_y1 = face_y1 - int(face_h*1.25)
        mask_y2 = mask_y1 + mask_height 

        #check to see if out of frame
        if mask_x1 < 0:
            mask_x1 = 0
        if mask_y1 < 0:
            mask_y1 = 0
        if mask_x2 > img_w:
            mask_x2 = img_w
        if mask_y2 > img_h:
            mask_y2 = img_h

        #Account for any out of frame changes
        mask_width = mask_x2 - mask_x1
        mask_height = mask_y2 - mask_y1

        #resize mask to fit on face
        mask = cv2.resize(mask, (mask_width,mask_height), interpolation = cv2.INTER_AREA)
        mask = cv2.resize(original_mask, (mask_width,mask_height), interpolation = cv2.INTER_AREA)
        mask_inv = cv2.resize(original_mask_inv, (mask_width,mask_height), interpolation = cv2.INTER_AREA)

        #take ROI for mask from background that is equal to size of mask image
        roi = img[mask_y1:mask_y2, mask_x1:mask_x2]

        #original image in background (bg) where mask is not
        roi_bg = cv2.bitwise_and(roi,roi,mask = mask)
        roi_fg = cv2.bitwise_and(mask,mask,mask=mask_inv)
        dst = cv2.add(roi_bg,roi_fg)

        #put back in original image
        img[mask_y1:mask_y2, mask_x1:mask_x2] = dst

        break
        
    #display image
    cv2.imshow('img',img) 

    #if user pressed 'q' break
    if cv2.waitKey(1) == ord('q'): # 
        break

gif.realease()
cap.release()
cv2.destroyAllWindows()