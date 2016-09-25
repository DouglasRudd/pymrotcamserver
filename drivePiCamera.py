#!/usr/bin/python
import io
import unittest
import driveCameraBase
import time
import picamera

class piCamera(driveCameraBase.cameraBase):
    def __init__(self, output=None):
        driveCameraBase.cameraBase.__init__(self, output)
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640,480)

    def __serve_method__(self):
        self.camera.capture(self.output,'jpeg')

    def __exit__(self):
        self.camera.close()

class piCameraTester(unittest.TestCase):
    def setUp(self):
        self.output = io.BytesIO()
        self.camera = piCamera(self.output)
        self.camera.serve_forever()

    def test_output_buffered(self):
        time.sleep(30)
        self.assertGreater(self.output.getvalue(), 0)

