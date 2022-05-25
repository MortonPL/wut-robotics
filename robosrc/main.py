#!/usr/bin/ micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from time import time
import sys
import signal
import argparse

from clock import tps, avgtps
from detector import Detector
from drive import Drive
from pid import PID

if __name__ == '__main__':
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', action='store', nargs='?',
                        choices=['black', 'color'], default='black', help='mode of action')
    parser.add_argument('--def-speed', action='store', nargs='?',
                        default=10, type=int, help='default speed')
    parser.add_argument('-p', '--printer', action='store', nargs='?',
                        choices=['mini', 'thin', 'pretty'], default='mini', help='extended (slow) diagnostics')
    args = vars(parser.parse_args())
    # switch modes
    if args['printer'] == 'pretty':
        from prettyprinter import Printer
    elif args['printer'] == 'thin':
        from thinprinter import Printer
    else:
        from minprinter import Printer

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

        def get_args(self, args):
            self.mode = args['mode']
            self.speeddiv = 0
            self.minspeed = 0
            self.defspeed = args['def_speed']

        def register_devices(self, drive, detector, button, printer):
            self.drive = drive
            self.detector = detector
            self.button = button
            self.printer = printer
        
        def calibrate_colors(self):
            self.printer.print_action("\u001b[36mSTART\u001b[0m STOCK CALIBRATION ?")
            input()
            self.printer.print_action("STOCK CALIBRATING ...")
            self.detector.calibrate_white()
            for mode in ['WHITE', 'BLACK', 'SOURCE', 'TARGET']:
                self.printer.print_action("\u001b[36mSTART\u001b[0m {} CALIBRATION ?".format(mode))
                input()
                self.printer.print_action("CALIBRATING {} ...".format(mode))
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
            self.print_init()
            
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

        def print_init(self):
            self.printer.print_layout()
            self.printer.print_args(args)

        def print_all(self, el, er, val_left, val_right, z, tps_, avg_):
            self.printer.print_rawcolor(self.detector.left.rgb, self.detector.right.rgb)
            self.printer.print_errors(el, er)
            self.printer.print_vals(val_left, val_right)
            self.printer.print_action_move(val_left, val_right, z)
            self.printer.print_time(tps_, avg_)


    def go_forth(robot):
        try:
            if robot.mode == "black":
                robot.main_black()
            elif robot.mode == "color":
                robot.main_color()
        except Exception as e:
            drive.stop()
            raise e

    ###################################################################
    # main body starts here
    signal.signal(signal.SIGINT, signal_handler)
    r = Robot()
    r.get_args(args)

    drive = Drive(OUTPUT_D, OUTPUT_A, r.minspeed, r.defspeed)
    drive.stop()
    detector = Detector(INPUT_4, INPUT_1)
    button = TouchSensor(INPUT_3)
    r.register_devices(drive, detector, button, Printer())
    r.calibrate_colors()
    r.printer.print_action("\u001b[31mSTART ROBOT ?\u001b[0m")
    input()

    go_forth(r)
