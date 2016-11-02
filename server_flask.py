from flask import Flask, render_template, Response
from time import time
app = Flask(__name__)

datas = [open('{0}.jpg'.format(i)).read() for i in range(1,6)]

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    #this object returned a generator
    while True:
        yield (b'--jpgboundary'
               b'Content-type: image/jpeg\r\n\r\n' + datas[int(time())%5 ] + b'\r\n')

@app.route('/cam.mjpg')
def feed_stream():
    print type(gen())
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=--jpgboundary')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


