#!/usr/bin/ micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from time import time
import sys
import signal

from clock import tps, avgtps
from detector import Detector
from drive import Drive
from pid import PID
from printer import pprint, pprint_action, pprint_errors, pprint_action_move, pprint_args, pprint_vals, pprint_layout, pprint_rawcolor, pprint_time

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
    mode = "black" # or "color"
    internal_mode = "go"

    # go           = follow black, seek source
    # found_source = follow source, await infrared contact
    # contact      = stop, pick up object
    # turn         = rotate 180 degrees
    # picked       = follow source, seek black
    # go_again     = follow black, seek target
    # found_target = follow target just for a bit
    # drop         = stop, put down object
    # exit


    def parse_args(self):
        if (len(sys.argv) > 1):
            self.mode = sys.argv[1]
            self.speeddiv = int(sys.argv[2])
            self.minspeed = int(sys.argv[3])
            self.defspeed = int(sys.argv[4])

    def register(self, drive, detector, button):
        self.drive = drive
        self.detector = detector
        self.button = button
    
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

    def init(self):
        pid_left = PID(Kp=0.3, Ki=0, Kd=0)
        pid_right = PID(Kp=0.3, Ki=0, Kd=0)
        tpser = tps(time())
        avger = avgtps()
        tpser.send(None)
        avger.send(None)
        pid_left.first(time())
        pid_right.first(time())
        z = int((100 / self.speeddiv) / 5)
        return pid_left, pid_right, tpser, avger, z

    def main_black(self):
        pid_left, pid_right, tpser, avger, z = self.init()
        
        while True:
            tick = time()

            # Reading sensors
            # Color detection - Cartesian distance in bounded 3D color space
            el, er = self.detector.get_distance()

            # Pid and steering control
            angle_left = pid_left.next(tick, 0, el) / 7
            angle_right = pid_right.next(tick, 0, er) / 7
            val_left = max(min(angle_left, 100), -100) / self.speeddiv # clamp to [-100, 100] and scale to [-20, 20]
            val_right = max(min(angle_right, 100), -100) / self.speeddiv # clamp to [-100, 100] and scale to [-20, 20]

            # Driving
            self.drive.correct(val_left, val_right)

            # Diagnostics
            tps_ = tpser.send(tick) # type: ignore
            self.print_all(el, er, val_left, val_right, z, tps_, avger.send(tps_))


    def main_color(self):
        pid_left, pid_right, tpser, avger, z = self.init()

        while True:
            tick = time()

    def print_all(self, el, er, val_left, val_right, z, tps_, avg_):
        pprint_rawcolor(self.detector.left.rgb, self.detector.right.rgb)
        pprint_errors(el, er)
        pprint_vals(val_left, val_right)
        pprint_action_move(val_left, val_right, z)
        pprint_time(tps_, avg_) # # PRINTPRINT


def go_forth(robot):
    try:
        if robot.mode == "black":
            robot.main_black()
        elif robot.mode == "color":
            robot.main_color()
    except Exception as e:
        drive.stop()
        raise e

if __name__ == '__main__':
    pprint_layout() # # PRINTPRINT
    signal.signal(signal.SIGINT, signal_handler)
    r = Robot()
    r.parse_args()
    pprint_args(r.mode, r.speeddiv, r.minspeed, r.defspeed)

    drive = Drive(OUTPUT_D, OUTPUT_A, r.minspeed, r.defspeed)
    drive.stop()
    detector = Detector(INPUT_4, INPUT_1)
    button = TouchSensor(INPUT_3)
    r.register(drive, detector, button)
    r.calibrate()
    pprint_action("\u001b[31mSTART ROBOT ?\u001b[0m") # # PRINTPRINT
    input()

    go_forth(r)
