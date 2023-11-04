import cv2 as cv
import keyboard

video = cv.VideoCapture(0)
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
while True :
    check,frame = video.read()
    face = face_cascade.detectMultiScale(frame,
    scaleFactor = 2,
    minNeighbors = 5)
    for x,y,w,h in face:
        frame = cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        cv.putText(frame,str("face"), (x,y-5),cv.FONT_HERSHEY_PLAIN, 2, (0,255,0),2)
    cv.imshow('Video',frame)
    key = cv.waitKey(1)
    if keyboard.is_pressed('Esc'):
        break

video.release()
cv.destroyAllWindows()