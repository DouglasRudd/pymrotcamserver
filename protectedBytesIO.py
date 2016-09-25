from multiprocessing.pool import ThreadPool
import random
import unittest
import io

import writerReaderLock

# decoration mode


class protectedBytesIO(io.BytesIO):
    def __init__(self, byteio):
        self.__byteio = byteio
        self.__lock = writerReaderLock.readWriteLock()

    def getvalue(self):
        self.__lock.reader_acquire()
        value = self.__byteio.getvalue()
        self.__lock.reader_release()
        return value

    def seek(self, offset, whence=0):
        # do nothing , bypass this operation , merged with write(b)
        pass

    def tell(self):
        return self.__byteio.tell()

    def write(self, b):
        self.__lock.writer_acquire()
        # rewind
        # self.__byteio.truncate(0)
        self.__byteio.seek(0)
        self.__byteio.truncate(0)
        self.__byteio.write(b)
        self.__lock.writer_release()


class protectedBytesIOTester(unittest.TestCase):
    def __writeValue(self):
        self.__correction = '{0:f}'.format(random.random())
        self.__protected.write(self.__correction)

    def __readValue(self):
        return self.__protected.getvalue()

    def setUp(self):
        raw = io.BytesIO()
        self.__correction = 0
        self.__protected = protectedBytesIO(raw)

    def test_write(self):
        self.__protected.write("test123")

    def test_seek(self):
        self.__protected.seek(0)

    def test_write_getvalue(self):
        for i in range(0, 10, 1):
            self.__writeValue()
            self.assertEqual(self.__correction, self.__readValue())
            # self.__correction = '{0:f}'.format(random.random())
            # self.__protected.write(self.__correction)
            # self.__answer = self.__protected.getvalue()
            # self.assertEqual(self.__correction, result)

    def test_write_getvalue_multi(self):
        pool = ThreadPool(processes=20)
        resultList = [pool.apply_async(self.__readValue, ()) for i in range(0, 5, 1)]
        pool.apply_async(self.__writeValue, ())
        resultList += [pool.apply_async(self.__readValue, ()) for i in range(0, 5, 1)]
        for result in resultList:
            self.assertEqual(result.get(), self.__correction, self.__correction)
