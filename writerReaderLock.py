import unittest
from threading import Lock
from threading import Event
import threading


class readWriteLock(object):
    def __init__(self):
        self.__writeExclusive = Event()
        self.__readerCounter_lock = Lock()
        self.__readerCounter = 0

    def writer_acquire(self):
        self.__writeExclusive.clear()
        isAllReaderExited = False
        # blocking until all reader had been out
        while not isAllReaderExited:
            with self.__readerCounter_lock:
                if self.__readerCounter == 0:
                    isAllReaderExited = True

    def writer_release(self):
        self.__writeExclusive.set()

    def reader_acquire(self):
        self.__writeExclusive.wait()
        with self.__readerCounter_lock:
            self.__readerCounter += 1

    def reader_release(self):
        with self.__readerCounter_lock:
            self.__readerCounter -= 1


class readWriteLockTester(unittest.TestCase):
    def setUp(self):
        self.__lock = readWriteLock()
        self.__value = 0
        self.__writer_thread = threading.Thread(target=self.__writer_method)

    def __writer_method(self):
        self.__value = 5

    def test_reading_when_writer_out(self):
        pass
