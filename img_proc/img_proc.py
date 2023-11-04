import cv2 as cv
import numpy as np

#Variables
video = cv.VideoCapture(0)
button_person = False
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
green = (0,255,0)

def display():
    while True :
        check,frame = video.read()
        face = face_cascade.detectMultiScale(frame,
        scaleFactor = 2,
        minNeighbors = 5)

        face_proc(face,frame)
        cv.namedWindow("Video")
        cv.setMouseCallback("Video",click_button)
        button(frame)
        cv.imshow('Video',frame)
        #exit
        key = cv.waitKey(1)
        if key == 27:  # 27 is the ASCII code for the 'esc' key
            break

    video.release()
    cv.destroyAllWindows()

def face_proc(face,frame):
    for x,y,w,h in face:
        if button_person is True:
            frame = cv.rectangle(frame,(x,y),(x+w,y+h),green,3)
            cv.putText(frame,str("face"), (x,y-5),cv.FONT_HERSHEY_PLAIN, 2,green,2)

def button(frame):
    #button
    polygon = np.array([[(20,20),(150,20),(150,75),(20,75)]])
    cv.fillPoly(frame,polygon,green)
    cv.putText(frame,"Face",(30,60),cv.FONT_HERSHEY_PLAIN,3,(255,255,255),2)

def click_button(event,x,y,flags,params):
    global button_person
    if event==cv.EVENT_FLAG_LBUTTON:
        polygon = np.array([[(20,20),(150,20),(150,75),(20,75)]])

        is_inside = cv.pointPolygonTest(polygon, (x,y), False)
        if is_inside>0:
            if button_person is False:
                 button_person = True
            else:
                button_person = False
     
display()