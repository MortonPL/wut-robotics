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
from printer import pprint, pprint_action, pprint_action_move, pprint_args, pprint_vals, pprint_layout, pprint_rawcolor, pprint_time
from robosrc.printer import pprint_errors

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drive.stop()
    sys.exit(0)

class Robot:
    # Globals zone
    drive = Drive(None, None)
    detector = Detector(None, None)
    speeddiv = 5
    minspeed = 1
    defspeed = 5

    def parse_args(self):
        if (len(sys.argv) > 1):
            self.speeddiv = int(sys.argv[1])
            self.minspeed = int(sys.argv[2])
            self.defspeed = int(sys.argv[3])

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
        pid_left = PID(Kp=1, Ki=0, Kd=0)
        pid_right = PID(Kp=1, Ki=0, Kd=0)

        tpser = tps(time())
        avger = avgtps()
        tpser.send(None)
        avger.send(None)
        pid_left.first(time())
        pid_right.first(time())

        z = int((100 / self.speeddiv) / 5)

        try:
            while True:
                tick = time()

                # Reading sensors
                pprint_rawcolor(self.detector.left.rgb, self.detector.right.rgb) # # PRINTPRINT
                el, er = self.detector.get_distance()
                pprint_errors(el, er) # # PRINTPRINT

                # Color detection - Cartesian distance in bounded 3D color space
                # pprint_color('UNKNOWN')

                # Pid and steering control
                angle_left = pid_left.next(tick, 0, el) / 7
                angle_right = pid_right.next(tick, 0, er) / 7
                val_left = max(min(angle_left, 100), -100) / self.speeddiv # clamp to [-100, 100] and scale to [-20, 20]
                val_right = max(min(angle_right, 100), -100) / self.speeddiv # clamp to [-100, 100] and scale to [-20, 20]

                pprint_vals(val_left, val_right) # # PRINTPRINT
                pprint_action_move(val_left, val_right, z) # # PRINTPRINT

                # Driving
                self.drive.correct(val_left, val_right)

                tps_ = tpser.send(tick) # type: ignore
                pprint_time(tps_, avger.send(tps_)) # # PRINTPRINT
        except Exception as e:
            drive.stop()
            raise e


if __name__ == '__main__':
    pprint_layout()
    signal.signal(signal.SIGINT, signal_handler)
    r = Robot()
    r.parse_args()
    pprint_args(r.speeddiv, r.minspeed, r.defspeed)

    drive = Drive(OUTPUT_D, OUTPUT_A, r.minspeed, r.defspeed)
    drive.stop()
    detector = Detector(INPUT_4, INPUT_1)
    r.register(drive, detector)
    r.calibrate()
    pprint_action("\u001b[31mSTART ROBOT ?\u001b[0m")
    input()
    r.main()
