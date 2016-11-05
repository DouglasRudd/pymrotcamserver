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

    def move(self,*args, **kwargs):
        if 'command' in kwargs:
            command = kwargs['command']
            if command == 'CENTRAL':
                self.__currentPosition = self.__central
            else:
                increment = kwargs['increment']
                self.__currentPosition += (self.__command_dictionary[command] * increment)
        elif 'mode' in kwargs:
            mode = kwargs['mode']
            quantity = kwargs['quantity']
            if mode == 'ABS':
                self.__currentPosition = quantity
            elif mode == 'REL':
                self.__currentPosition += quantity

        self.__over_travel()
        return self.CurrentPosition

    def __over_travel(self):
        if self.__currentPosition < self.__soft_limit_minus:
            self.__currentPosition = self.__soft_limit_minus
        if self.__currentPosition > self.__soft_limit_plus:
            self.__currentPosition = self.__soft_limit_plus
        return self.CurrentPosition


class servo_axis_control_tester(unittest.TestCase):
    def setUp(self):
        self.__servo = servo_axis_control(central=1500)

    def test_forward(self):
        self.__servo.move(command='CENTRAL')
        self.assertEqual(self.__servo.move(command='FORWARD',increment=50),1550)

    def test_backward(self):
        self.__servo.move('CENTRAL')
        self.assertEqual(self.__servo.move(command='BACKWARD',increment=50),1450)

    def test_abs(self):
        self.__servo.move('CENTRAL')
        self.assertEqual(self.__servo.move(mode='ABS',quantity=1300),1300)
        self.assertEqual(self.__servo.move(mode='ABS',quantity=1900),1900)

    def test_rel(self):
        self.__servo.move('CENTRAL')
        self.assertEqual(self.__servo.move(mode='REL',quantity=100),1600)
        self.assertEqual(self.__servo.move(mode='REL',quantity=-200),1400)




