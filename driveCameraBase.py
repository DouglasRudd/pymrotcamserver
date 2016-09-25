import threading
import time

class cameraBase:
    def __init__(self, output=None,fps=60):
        self.output = output
        self.__interval = 1/fps

    def serve_forever(self):
        # initialize thread , run method
        def runningCallBack():
            while True:
                try:
                    self.__serve_method__()
                    time.sleep(self.__interval)
                except KeyboardInterrupt:
                    break
            return

        self.runningThread = threading.Thread(target=runningCallBack)
        self.runningThread.daemon = True
        self.runningThread.start()

    def __serve_method__(self):
        # function should be implemented by derived class
        pass
