#!/usr/bin/python
'''
Author: Igor Maculan - n3wtron@gmail.com
A Simple mjpg stream http server
'''
import io
import unittest
import driveCameraBase
import cv2
from PIL import Image
import time


class cvCamera(driveCameraBase.cameraBase):
    def __init__(self, output=None, gray_handler=lambda gray_image: gray_image):
        driveCameraBase.cameraBase.__init__(self, output)
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        self.capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        self.capture.set(cv2.cv.CV_CAP_PROP_SATURATION, 0.2)
        self.capture.set(cv2.cv.CV_CAP_PROP_FPS, 10)
        # event handler
        self.__gray_handler = gray_handler

    def __serve_method__(self):
        # self.output.seek(0)
        rc, img = self.capture.read()
        if rc:
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.__gray_handler(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            jpg = Image.fromarray(imgRGB)
            jpg.save(self.output, 'jpeg')


class cvCameraTester(unittest.TestCase):
    def setUp(self):
        self.output = io.BytesIO()
        self.camera = cvCamera(self.output)
        self.camera.serve_forever()
        print "setUp Finished"

    def test_output_buffered(self):
        time.sleep(30)
        self.assertGreater(self.output.getvalue(), 0)

