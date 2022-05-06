from ev3dev2.sensor.lego import ColorSensor

class Detector:
    left_sensor = ColorSensor()
    right_sensor = ColorSensor()

    def __init__(self, left_color_sensor_addr, right_color_sensor_addr):
        self.left_sensor = ColorSensor(left_color_sensor_addr)
        self.right_sensor = ColorSensor(right_color_sensor_addr)

    def left(self):
        return self.left_sensor.reflected_light_intensity

    def right(self):
        return self.right_sensor.reflected_light_intensity
