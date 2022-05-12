#!/usr/bin/ micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4
from time import time
import sys
import signal

from detector import Detector
from drive import Drive
from pid import PID
from printer import pprint_action, pprint_action_move, pprint_args, pprint_layout, pprint_sensor
from robosrc.printer import pprint_color

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drive.stop()
    sys.exit(0)

class Robot:
    # Globals zone
    light_threshold = 20
    normal_speed = 20
    slow_speed = 5
    high_speed = 10
    rot_speed = 0.01
    drive = Drive(None, None)
    detector = Detector(None, None)

    def parse_args(self):
        self.light_threshold = int(sys.argv[1])
        self.normal_speed = int(sys.argv[2])
        self.slow_speed = int(sys.argv[3])
        self.high_speed = int(sys.argv[4])
        self.rot_speed = float(sys.argv[5])

    def register(self, drive, detector):
        self.drive = drive
        self.detector = detector
    
    def calibrate(self):
        pprint_action("START STOCK CALIBRATION ?")
        input()
        self.detector.calibrate_white()
        for mode in ['WHITE ', 'BLACK ', 'SOURCE', 'TARGET']:
            pprint_action("START {0} CALIBRATION ?".format(mode))
            input()
            self.detector.calibrate(mode)
        
    def main(self):
        pid = PID(Kp=1, Ki=1, Kd=1)

        while True:
            # Reading sensors
            left_rgb = self.detector.left.rgb
            right_rgb = self.detector.right.rgb
            pprint_sensor(left_rgb, right_rgb)

            # Color detection - Euclidan distance in bounded 3D color space
            pprint_color('UNKNOWN')

            # Pid and steering control
            angle = pid.next(time, 1, 0)

            pprint_action_move(angle)
            
            # Driving
            self.drive.correct(angle)


if __name__ == '__main__':
    pprint_layout()
    signal.signal(signal.SIGINT, signal_handler)
    r = Robot()
    if (len(sys.argv) > 1):
        r.parse_args()
    pprint_args(r.slow_speed, r.normal_speed, r.high_speed, r.rot_speed)

    drive = Drive(OUTPUT_A, OUTPUT_D, r.slow_speed, r.normal_speed, r.high_speed, r.rot_speed)
    detector = Detector(INPUT_1, INPUT_4)
    r.register(drive, detector)
    r.calibrate()
    r.main()
