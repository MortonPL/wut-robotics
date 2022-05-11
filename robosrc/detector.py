from ev3dev2.sensor.lego import ColorSensor

def tuplemul(tup, num):
    return tuple(x * num for x in tup)

def tuplediv(tup, num):
    return tuple(x / num for x in tup)

class Detector:
    left = ColorSensor()
    right = ColorSensor()
    white = (0, 0, 0)
    black = (0, 0, 0)
    source = (0, 0, 0)
    target = (0, 0, 0)
    sampling_size = 100

    def __init__(self, left_color_sensor_addr, right_color_sensor_addr):
        self.left = ColorSensor(left_color_sensor_addr)
        self.right = ColorSensor(right_color_sensor_addr)

    def calibrate_white(self):
        self.left.calibrate_white()
        self.right.calibrate_white()

    def calibrate(self, mode):
        array = [(0, 0, 0)] * self.sampling_size
        for i in range(self.sampling_size):
            array[i] = tuplemul(self.left.rgb + self.right.rgb, self.sampling_size)

        if mode == "white":
            self.white = tuplediv(sum(array), len(array))
        elif mode == "black":
            self.black = tuplediv(sum(array), len(array))
        elif mode == "source":
            self.source = tuplediv(sum(array), len(array))
        elif mode == "target":
            self.target = tuplediv(sum(array), len(array))
