
WIDTH = 320
HEIGHT = 160

CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2
try:
    # pi enviroment
    import pigpio
    import picamera
    import picamera.array
    piController = pigpio.pi()
    piCam = picamera.PiCamera()
    piCam.resolution = (WIDTH, HEIGHT)
    # piCam.start_preview()
except ImportError:
    # non-pi enviroment
    # FIXME : implemnt some virtual devices
    pass


from gevent import monkey
import gevent.wsgi
import gevent
monkey.patch_all()

from flask import Flask, render_template, Response
import time
import cv2
from PIL import Image
import io

import axis_controll
axisX = axis_controll.servo_axis_control()
axisY = axis_controll.servo_axis_control()


output =io.BytesIO()
output_array = picamera.array.PiRGBArray(piCam)
# cam = driveCvCamera.cvCamera(output)

# capture = cv2.VideoCapture(0)
# capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
# capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
# capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)
# capture.set(cv2.cv.CV_CAP_PROP_FPS, 10)

face_detect = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

def video_capturing():
    while True:
        # rc, img = capture.read()
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        time.clock()
        output_array.truncate(0)
        piCam.capture(output_array,'rgb')
        img = output_array.array
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        print 'capture/convert:{0}'.format(time.clock())

        objects = face_detect.detectMultiScale(
            img_gray,
            scaleFactor=1.1,
            minNeighbors=1,
        )
        print 'face_detect:{0}'.format(time.clock())

        if len(objects) >= 1:
            for x, y, w, h in objects:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            print 'rectangle:{0}'.format(time.clock())

            x, y, w, h = objects[0]

            __center_x = x+w/2
            __center_y = y+h/2
            #face trakcing
            diff_x = 1.2*(CENTER_X-__center_x)
            diff_y = -0.3*(CENTER_Y-__center_y)
            print (__center_x,
                   __center_y,
                   diff_x,
                   diff_y,
                   img.shape[0],
                   img.shape[1],
                   axisX.CurrentPosition,
                   axisY.CurrentPosition)
            axisX.move(mode='REL', quantity=diff_x)
            axisY.move(mode='REL', quantity=diff_y)

            piController.set_servo_pulsewidth(16, axisX.CurrentPosition)
            piController.set_servo_pulsewidth(20, axisY.CurrentPosition)
            print 'servo:{0}'.format(time.clock())

        output.seek(0)
        output.truncate(0)
        Image.fromarray(img).save(output,'jpeg')
        print 'jpeg:{0}'.format(time.clock())
        gevent.sleep(0.05)
        # time.sleep(0.2)


app = Flask(__name__)

# datas = [open('{0}.jpg'.format(i)).read() for i in range(1,6)]

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
    piController.set_servo_pulsewidth(16, 1500)
    piController.set_servo_pulsewidth(20, 1500)

    # video_capturing()
    th_video = gevent.spawn(video_capturing)
    # th_app = gevent.spawn(app.run,'')
    print 'spawn'
    # gevent.joinall([th_app,th_video])
    server = gevent.pywsgi.WSGIServer(('', 8060), app)
    server.serve_forever()


