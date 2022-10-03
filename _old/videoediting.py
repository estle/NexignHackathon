import glob

import cv2
import os


def render():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    cdir = os.getcwd()
    witch = cv2.imread(cdir + "/images/what.png")

    original_witch_h, original_witch_w, witch_channels = witch.shape

    witch_gray = cv2.cvtColor(witch, cv2.COLOR_BGR2GRAY)

    ret, original_mask = cv2.threshold(witch_gray, 10, 255, cv2.THRESH_BINARY_INV)
    original_mask_inv = cv2.bitwise_not(original_mask)

    cap = cv2.VideoCapture(cdir + "/wow.mp4")
    ret, img = cap.read()
    img_h, img_w = img.shape[:2]
    out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (img_w, img_h))

    while True:
        ret, img = cap.read()
        if ret == False: break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:

            face_w = w
            face_h = h
            face_x1 = x
            face_x2 = face_x1 + face_w
            face_y1 = y
            face_y2 = face_y1 + face_h

            witch_width = int(1.5 * face_w)
            witch_height = int(witch_width * original_witch_h / original_witch_w)

            witch_x1 = face_x2 - int(face_w / 2) - int(witch_width / 2)
            witch_x2 = witch_x1 + witch_width
            witch_y1 = face_y1 - int(face_h * 1.25)
            witch_y2 = witch_y1 + witch_height

            if witch_x1 < 0:
                witch_x1 = 0
            if witch_y1 < 0:
                witch_y1 = 0
            if witch_x2 > img_w:
                witch_x2 = img_w
            if witch_y2 > img_h:
                witch_y2 = img_h

            witch_width = witch_x2 - witch_x1
            witch_height = witch_y2 - witch_y1

            witch = cv2.resize(witch, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            mask = cv2.resize(original_mask, (witch_width, witch_height), interpolation=cv2.INTER_AREA)
            mask_inv = cv2.resize(original_mask_inv, (witch_width, witch_height), interpolation=cv2.INTER_AREA)

            roi = img[witch_y1:witch_y2, witch_x1:witch_x2]

            roi_bg = cv2.bitwise_and(roi, roi, mask=mask)
            roi_fg = cv2.bitwise_and(witch, witch, mask=mask_inv)
            dst = cv2.add(roi_bg, roi_fg)

            img[witch_y1:witch_y2, witch_x1:witch_x2] = dst

            break

        cv2.imwrite('image.png', img)

        for filename in glob.glob('image.png'):
            img = cv2.imread(filename)
            out.write(img)

        # cv2.imshow('img', img)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
