import time
import cv2
import gevent
from gevent import monkey

monkey.patch_all()

capture = cv2.VideoCapture(0)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)
capture.set(cv2.cv.CV_CAP_PROP_FPS, 10)

face_detect = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

def video_capturing():
    while True:
        rc, img = capture.read()
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        objects = face_detect.detectMultiScale(
            img_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        for x,y,w,h in objects:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        cv2.imshow('img', img)
        # once start to sleep here , then video_capturing would be blocked
        # otherwise , just_counting would be blocked
        # gevent.sleep(1)


def just_counting(__counter):
    while True:
        __counter += 1
        print __counter
        gevent.sleep(1)

if __name__ == '__main__':
    counter1 = 0
    counter2 = 0
    # th0 = gevent.spawn(just_counting, counter1)
    # th2 = gevent.spawn(just_counting, counter2)
    # th1 = gevent.spawn(video_capturing)
    # gevent.joinall([th2, th0, th1])
    video_capturing()
    # while True:
        # rc,img = capture.read()
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        # cv2.imshow('img', img)
    # cv2.waitKey(0)
