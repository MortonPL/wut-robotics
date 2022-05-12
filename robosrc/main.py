#!/usr/bin/ micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4
from time import time, sleep
import sys
import signal

from clock import tps, avgtps
from detector import Detector
from drive import Drive
from pid import PID
from printer import pprint, pprint_action, pprint_action_move, pprint_args, pprint_color, pprint_layout, pprint_sensor, pprint_time

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
    rot_speed = 0.0001
    drive = Drive(None, None)
    detector = Detector(None, None)

    def parse_args(self):
        if (len(sys.argv) > 1):
            self.light_threshold = int(sys.argv[1])
            self.normal_speed = int(sys.argv[2])
            self.slow_speed = int(sys.argv[3])
            self.high_speed = int(sys.argv[4])
            self.rot_speed = float(sys.argv[5])

    def register(self, drive, detector):
        self.drive = drive
        self.detector = detector
    
    def calibrate(self):
        pprint_action("\u001b[36mSTART\u001b[0m STOCK CALIBRATION ?")
        input()
        pprint_action("STOCK CALIBRATING ...")
        self.detector.calibrate_white()
        for mode in ['WHITE', 'BLACK', 'SOURCE', 'TARGET']:
            pprint_action("\u001b[36mSTART\u001b[0m {} CALIBRATION ?".format(mode))
            input()
            pprint_action("CALIBRATING {} ...".format(mode))
            self.detector.calibrate(mode)
        
    def main(self):
        pid = PID(Kp=1, Ki=0, Kd=0)

        tpser = tps(time())
        avger = avgtps()
        tpser.send(None)
        avger.send(None)
        pid.first(time())

        while True:
            tick = time()

            # Reading sensors
            pprint_sensor(self.detector.left.rgb, self.detector.right.rgb)
            e = self.detector.get_distance()
            print(e)

            # Color detection - Euclidan distance in bounded 3D color space
            pprint_color('UNKNOWN')

            # Pid and steering control
            angle = pid.next(tick, 0, e) / 2

            pprint_action_move(angle)
            
            # Driving
            self.drive.correct(angle)

            tps_ = tpser.send(tick) # type: ignore
            pprint_time(tps_, avger.send(tps_))
            sleep(0.1)


if __name__ == '__main__':
    pprint_layout()
    signal.signal(signal.SIGINT, signal_handler)
    r = Robot()
    r.parse_args()
    pprint_args(r.slow_speed, r.normal_speed, r.high_speed, r.rot_speed)

    drive = Drive(OUTPUT_A, OUTPUT_D, r.slow_speed, r.normal_speed, r.high_speed, r.rot_speed)
    detector = Detector(INPUT_1, INPUT_4)
    r.register(drive, detector)
    r.calibrate()
    pprint_action("\u001b[31mSTART ROBOT ?\u001b[0m")
    input()
    r.main()
