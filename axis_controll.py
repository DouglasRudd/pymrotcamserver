import unittest


class servo_axis_control:
    def __init__(self, central=1500, soft_limit_plus=2000, soft_limit_minus=1000):
        self.__currentPosition = central
        self.__central = central
        self.__soft_limit_plus = soft_limit_plus
        self.__soft_limit_minus = soft_limit_minus
        self.__command_dictionary = {'FORWARD':1, 'BACKWARD':-1}

    def __str__(self):
        return "%s;%s" % (self, self.__increment)

    @property
    def CurrentPosition(self):
        return self.__currentPosition

    def move(self, command, increment=50):
        # self.__currentPosition += ((int(forward == True) - 0.5) * 2) * increment
        if command == 'CENTRAL':
            self.__currentPosition = self.__central
        else:
            self.__currentPosition += (self.__command_dictionary[command] * increment)
            if self.__currentPosition < self.__soft_limit_minus:
                self.__currentPosition = self.__soft_limit_minus
            if self.__currentPosition > self.__soft_limit_plus:
                self.__currentPosition = self.__soft_limit_plus

        return self.CurrentPosition


class servo_axis_control_tester(unittest.TestCase):
    def setUp(self):
        self.__servo = servo_axis_control(central=1500)

    def test_forward(self):
        self.__servo.move('CENTRAL')
        self.assertEqual(self.__servo.move('FORWARD'), 1550)

    def test_backward(self):
        self.__servo.move('CENTRAL')
        self.assertEqual(self.__servo.move('BACKWARD'), 1450)

