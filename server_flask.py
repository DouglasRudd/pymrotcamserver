from gevent import monkey
import gevent.wsgi
import gevent
monkey.patch_all()

from flask import Flask, render_template, Response
from time import time
import cv2
from PIL import Image
# import driveCvCamera
import io

output =io.BytesIO()
# cam = driveCvCamera.cvCamera(output)

capture = cv2.VideoCapture(0)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)
capture.set(cv2.cv.CV_CAP_PROP_FPS, 10)

face_detect = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

def video_capturing():
    while True:
        rc, img = capture.read()
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
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

        # cv2.imshow('img', img)
        # once start to sleep here , then video_capturing would be blocked
        # otherwise , just_counting would be blocked
        output.seek(0)
        output.truncate(0)
        Image.fromarray(img).save(output,'jpeg')
        print 'video_capturing'
        gevent.sleep(1)


app = Flask(__name__)

datas = [open('{0}.jpg'.format(i)).read() for i in range(1,6)]

def test():
    while True:
        print '1'
        gevent.sleep(1)

@app.route('/')
def index():
    print 'index'
    return render_template('index.html')

def gen():
    #this object returned a generator
    while True:
        # __data = datas[int(time())%5 ]
        __data = output.getvalue()
        yield (b'--jpgboundary'
               b'Content-type: image/jpeg\r\n\r\n' + __data + b'\r\n')

@app.route('/cam.mjpg')
def feed_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')

if __name__ == '__main__':
    th_video = gevent.spawn(video_capturing)
    # th_cam = gevent.spawn(cam.serve_forever)
    # th_app = gevent.spawn(app.run,'')
    # th_test = gevent.spawn(test)
    print 'spawn'
    # gevent.joinall([th_app,th_cam])
    server = gevent.pywsgi.WSGIServer(('',5000),app)
    server.serve_forever()
    # app.run('',threaded=True)


