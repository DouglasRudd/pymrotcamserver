import joystickCommandPack

class buttonIncrementor:
    def __init__(self, central=1500, __increment=50):
        self.currentPosition = central
        self.increment = __increment
    def __str__(self):
        return "%s;%s" % (self.currentPosition, self.increment)
    def move(self, forward):
        self.currentPosition += ((int(forward == True) - 0.5) * 2) * self.increment
        if self.currentPosition < 500:
            self.currentPosition = 500
        if self.currentPosition > 2500:
            self.currentPosition = 2500
        return self.currentPosition
