import cv2
import unittest


class face_detect_handler(object):
    def __init__(self):
        self.__face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    def handle_face(self, gray_image):
        faces = self.__face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        #take first x,y
        # return faces[0][0], faces[0][1]
        return faces

class face_detect_handler_tester(unittest.TestCase):
    def setUp(self):
        self.__face_d = face_detect_handler()

    def test_function(self):
        print self.__face_d.handle_face(cv2.cvtColor(
            cv2.imread('./abba.png'),
            cv2.COLOR_BGR2GRAY
        ))
