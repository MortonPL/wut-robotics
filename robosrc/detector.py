from ev3dev2.sensor.lego import ColorSensor
from math import sqrt

def tupleadd(tup1, tup2):
    return (tup1[0] + tup2[0], tup1[1] + tup2[1], tup1[2] + tup2[2])

def tuplemul(tup, num):
    return tuple(x * num for x in tup)

def tuplediv(tup, num):
    return tuple(x / num for x in tup)

def dist3d(tup1, tup2):
    return sqrt((tup1[0] - tup2[0])**2 + (tup1[1] - tup2[1])**2 + (tup1[2] - tup2[2])**2)


class Detector:
    left = ColorSensor()
    right = ColorSensor()
    white = (0, 0, 0)
    black = (0, 0, 0)
    source = (0, 0, 0)
    target = (0, 0, 0)
    SAMPLING_SIZE = 10
    color = black

    def __init__(self, left_color_sensor_addr, right_color_sensor_addr):
        self.left = ColorSensor(left_color_sensor_addr)
        self.right = ColorSensor(right_color_sensor_addr)

    def calibrate_white(self):
        self.left.calibrate_white()
        self.right.calibrate_white()

    def calibrate(self, mode):
        y = (0,0,0)

        for i in range(self.SAMPLING_SIZE):
            y = tupleadd(tuplediv(tupleadd(self.left.rgb, self.right.rgb), 2), y)

        if mode == "WHITE":
            self.white = tuplediv(y, self.SAMPLING_SIZE)
        elif mode == "BLACK":
            self.black = tuplediv(y, self.SAMPLING_SIZE)
        elif mode == "SOURCE":
            self.source = tuplediv(y, self.SAMPLING_SIZE)
        elif mode == "TARGET":
            self.target = tuplediv(y, self.SAMPLING_SIZE)

    def get_distance(self):
        return dist3d(self.left.rgb, self.color), dist3d(self.right.rgb, self.color)

    def find_color(self):
        lblack, rblack = dist3d(self.left.rgb, self.black), dist3d(self.right.rgb, self.black)
        lsource, rsource = dist3d(self.left.rgb, self.source), dist3d(self.right.rgb, self.source)
        ltarget, rtarget = dist3d(self.left.rgb, self.target), dist3d(self.right.rgb, self.target)
        
