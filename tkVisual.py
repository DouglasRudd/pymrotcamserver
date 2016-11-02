import face_detect
import driveCvCamera
import io
import time
import cv2
import gevent
from gevent import monkey

monkey.patch_all()

counter = 0

def func(imgRGB=None):
    coord = fd.handle_face(cv2.cvtColor(imgRGB, cv2.COLOR_RGB2GRAY))
    if len(coord) > 1:
        x,y,w,h = tuple(coord[0])
        cv2.circle(imgRGB, (x,y), 50, (0, 255, 0))
        print 'coord{0},{1}'.format(x,y)
    cv2.imshow('image',imgRGB)



def counting(__counter):
    while True:
        __counter += 1
        print __counter
        time.sleep(1)

fd = face_detect.face_detect_handler()
cam_output = io.BytesIO()
cam = driveCvCamera.cvCamera(output=cam_output,gray_handler=func)

if __name__ == '__main__':
    counter1 = 0
    counter2 = 0
    # th0 = gevent.spawn(counting,counter1)
    # th2 = gevent.spawn(counting,counter2)
    # th1 = gevent.spawn(cam.serve_forever)
    # gevent.joinall([th2,th0,th1])
    # time.sleep(60)
    # print 'joinall'
    cam.serve_forever()
    # time.sleep(60)
    # print 'timeout'
