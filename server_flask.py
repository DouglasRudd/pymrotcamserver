
WIDTH = 320
HEIGHT = 160

CENTER_X = WIDTH/2
CENTER_Y = HEIGHT/2

CHANNEL_X = 16
CHANNEL_Y = 20

ENV ='non-pi'

try:
    # pi enviroment
    import pigpio
    import picamera
    import picamera.array
    piController = pigpio.pi()
    piCam = picamera.PiCamera()
    piCam.resolution = (WIDTH, HEIGHT)
    output_array = picamera.array.PiRGBArray(piCam)
    # piCam.start_preview()
    ENV = 'pi'
except ImportError:
    # non-pi enviroment
    # FIXME : implemnt some virtual devices
    ENV = 'non-pi'


from gevent import monkey
import gevent.wsgi
import gevent
monkey.patch_all()

from flask import Flask, render_template, Response, request, jsonify, g
import time
import cv2
from PIL import Image
import io
import logging

import axis_controll
axisX = axis_controll.servo_axis_control()
axisY = axis_controll.servo_axis_control()
axis_collection = [axisX,axisY]
axis_dictionary = {}
axis_dictionary['X'] = axisX
axis_dictionary['Y'] = axisY
axis_dictionary['mode'] = "Manual"

output =io.BytesIO()

if ENV == 'non-pi':
    capture = cv2.VideoCapture(0)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
    capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)
    capture.set(cv2.cv.CV_CAP_PROP_FPS, 10)

face_detect = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

def video_capturing():
    while True:
        start=time.clock()

        if ENV == 'non-pi':
            rc, img = capture.read()
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        else :
            output_array.truncate(0)
            piCam.capture(output_array,'rgb')
            img = output_array.array

        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        logging.info('capture/convert:{0}'.format(time.clock()-start))

        start=time.clock()
        objects = face_detect.detectMultiScale(
            img_gray,
            scaleFactor=1.6,
            minNeighbors=1,
        )
        logging.info('face_detect:{0}'.format(time.clock()-start))

        if len(objects) >= 1:
            start=time.clock()
            for x, y, w, h in objects:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            logging.info('rectangle:{0}'.format(time.clock()-start))

            x, y, w, h = objects[0]

            __center_x = x+w/2
            __center_y = y+h/2
            #face trakcing
            diff_x = 1.2*(CENTER_X-__center_x)
            diff_y = -0.3*(CENTER_Y-__center_y)
            logging.info(__center_x,
                   __center_y,
                   diff_x,
                   diff_y,
                   img.shape[0],
                   img.shape[1],
                   axisX.CurrentPosition,
                   axisY.CurrentPosition)
            #output compensation
            if axis_dictionary['mode'] == 'Auto' :
                axisX.move(mode='REL', quantity=diff_x)
                axisY.move(mode='REL', quantity=diff_y)

        #output mjpeg
        start=time.clock()
        output.seek(0)
        output.truncate(0)
        Image.fromarray(img).save(output,'jpeg')
        logging.info('jpeg:{0}'.format(time.clock()-start))
        gevent.sleep(0.02)

def servo_output():
    while True:
        start=time.clock()
        piController.set_servo_pulsewidth(CHANNEL_X, axisX.CurrentPosition)
        piController.set_servo_pulsewidth(CHANNEL_Y, axisY.CurrentPosition)
        logging.info('servo:{0}'.format(time.clock()-start))
        gevent.sleep(0.1)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control',methods=['POST'])
def control():
    # print request.form
    __axis = request.form['axis']
    __mode = request.form['coord']
    __quantity = float(request.form['direction']) * float(request.form['angle'])
    axis_dictionary[__axis].move(mode=__mode,quantity=__quantity)
    axis_dictionary['mode'] = str(request.form['mode'])
    # logging.debug(__axis,__mode,__quantity,g.mode)
    return 'done'

@app.route('/position')
def position():
    return jsonify(X=axisX.CurrentPosition,
                   Y=axisY.CurrentPosition)

def gen():
    #this object returned a generator
    while True:
        __data = output.getvalue()
        yield (b'--jpgboundary'
               b'Content-type: image/jpeg\r\n\r\n' + __data + b'\r\n')

@app.route('/cam.mjpg')
def feed_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')

if __name__ == '__main__':
    # video_capturing()
    # corroutine flask server and camera/fact_detect
    if ENV == 'pi':
        th_servo = gevent.spawn(servo_output)
    else:
        pass
    th_video = gevent.spawn(video_capturing)
    server = gevent.pywsgi.WSGIServer(('', 8060), app)
    server.serve_forever()


