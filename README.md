# pymrotcamserver
Simple 2-axis motorized rotating camera MJPG server on raspberry pi , motion parts depends on pigpio library.<br> 
Camera capture function also can be tested on non-pi enviroment by the helps of cv2 (python wrapper of OpenCV).<br>
Going to have some fun features further , such as motorized face-tracking , click-and-set image center , or do some further complex image process.<br>

***

# Depedencies (raspberry/rasbian)

+ OpenCV/cv2:
    + usage:
        + face-detect
    + reference: 
        + http://trevorappleton.blogspot.tw/2013/11/python-getting-started-with-opencv.html
    + installation: 
        + $sudo apt-get install libopencv-dev python-opencv

+ PIL/pillow:
    + usage:
        + array image to jpeg stream conversion
    + installation:
        + $pip install pillow

+ gevent:
    + usage:
        + coherence framework of flask WSGI server and face-tracking routine
    + installation:
        + $pip install gevent

+ flask:
    + usage:
        + framework of http server
    + installation:
        + $pip install flask

+ pigpiod:
    + usage:
        + servo motor driven
    + reference:
        + http://abyz.co.uk/rpi/pigpio/download.html 
    + installation:
        + apt-get install pigpio python-pigpio python3-pigpio

***

# Start to use

>Step1 , activate pigpio daemon for motor driven
>>$sudo pigpiod

>Step2 , start the server , which included face detect routine
>>$python server_flask.py