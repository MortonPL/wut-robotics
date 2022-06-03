#!/usr/bin/ micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import InfraredSensor
from time import time, sleep
import sys
import signal
import argparse

from clock import tps, avgtps
from detector import Detector
from drive import Drive
from pid import PID

#######################################################################################

if __name__ == '__main__':
    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', action='store', nargs='?',
                        choices=['black', 'color'], default='black', help='mode of action')
    parser.add_argument('--def-speed', action='store', nargs='?',
                        default=7, type=float, help='default speed')
    parser.add_argument('--turn-mod', action='store', nargs='?',
                        default=1.7, type=float, help='turn modifier')
    parser.add_argument('--turn-flat', action='store', nargs='?',
                        default=1, type=float, help='turn modifier')
    parser.add_argument('-p', '--printer', action='store', nargs='?',
                        choices=['mini', 'thin'], default='mini', help='extended (slow) diagnostics')
    args = vars(parser.parse_args())
    # switch modes
    if args['printer'] == 'thin':
        from thinprinter import Printer
    else:
        from minprinter import Printer

    def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        drive.stop()
        sys.exit(0)

#######################################################################################

    class Robot:
        # Globals zone
        drive = Drive(None, None, None, None, None)
        detector = Detector(None, None)
        claw = MediumMotor(OUTPUT_B)
        #button = TouchSensor()
        infraredSensor = InfraredSensor(INPUT_3)
        state = "go"

        def get_args(self, args):
            self.mode = args['mode']
            self.defspeed = args['def_speed']
            self.turnmod = args['turn_mod']
            self.turnflat = args['turn_flat']

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
            pid_left = PID(Kp=0.25, Ki=0, Kd=0)
            pid_right = PID(Kp=0.25, Ki=0, Kd=0)
            tpser = tps(time())
            avger = avgtps()
            tpser.send(None)
            avger.send(None)
            pid_left.first(time())
            pid_right.first(time())
            return pid_left, pid_right, tpser, avger

#######################################################################################

        def main_black(self):
            pid_left, pid_right, tpser, avger = self.init()
            self.print_init()
            self.go_drive(pid_left, pid_right, tpser, avger, lambda _: False, 0)

#######################################################################################
        # 1 seek_source     = follow black, seek source
        # 2 follow_source   = follow source up to the square
        # 3 enter_source    = go forward, await infrared contact
        # 4 contact         = stop, pick up object, rotate 180 degrees
        # 5 exit_source     = go forward, await source line
        # 6 follow_source_2 = follow source, seek black
        # 7 seek_target     = follow black, seek target
        # 8 follow_target   = follow target up to the square
        # 9 enter_target    = go forward, a bit
        # 10 drop           = stop, put down object

        # 1 ==== 2/7 ======= 8 =======
        #         S          T
        #         S          T
        #         S          T
        #     SS 3/6 SS   TT 9  TT
        #     SS 4/5 SS   TT 10 TT
        #     SSSSSSSSS   TTTTTTTT


        def main_color(self):
            pid_left, pid_right, tpser, avger = self.init()
            self.claw.on_to_position(SpeedPercent(-10), 0)

            l, r = self.state_seek_source(pid_left, pid_right, tpser, avger)
            side = 'l'
            if l > r: # type:ignore
                side = 'r'
            self.state_rotate_90(pid_left, pid_right, tpser, avger, side)
            self.state_follow_source(pid_left, pid_right, tpser, avger)
            self.state_enter_source(pid_left, pid_right, tpser, avger)
            self.state_contact()
            self.state_exit_source(pid_left, pid_right, tpser, avger)
            self.state_follow_source_2(pid_left, pid_right, tpser, avger)

            if side == 'l':
                side = 'r'
            else:
                side = 'l'
            self.state_rotate_90(pid_left, pid_right, tpser, avger, side)
            self.state_seek_target(pid_left, pid_right, tpser, avger)
            self.state_follow_target(pid_left, pid_right, tpser, avger)
            self.state_enter_target(pid_left, pid_right, tpser, avger)
            self.state_drop()

            return

            self.state_seek_source(pid_left, pid_right, tpser, avger)
            self.state_follow_source(pid_left, pid_right, tpser, avger)
            self.state_enter_source(pid_left, pid_right, tpser, avger)
            self.state_contact()
            self.state_exit_source(pid_left, pid_right, tpser, avger)
            self.state_follow_source_2(pid_left, pid_right, tpser, avger)
            self.state_seek_target(pid_left, pid_right, tpser, avger)
            self.state_follow_target(pid_left, pid_right, tpser, avger)
            self.state_enter_target(pid_left, pid_right, tpser, avger)
            self.state_drop()

            # 7 - optimal distance; 22 - casual distance

        # follow the line until you find source color
        def state_seek_source(self, pid_left, pid_right, tpser, avger):
            self.state = "seek_source"
            def cond(r):
                sl, sr = r.detector.get_distance(1)
                return sl < 100 or sr < 100                                    # TODO FIND GOODENOUGH VALUES
            return self.go_drive(pid_left, pid_right, tpser, avger, cond, 0, 1)

        # turn 90 degrees
        def state_rotate_90(self, pid_left, pid_right, tpser, avger, side):
            self.state = "turn_90"
            self.drive.rotate90(side)

        # follow the source line until square
        def state_follow_source(self, pid_left, pid_right, tpser, avger):
            self.state = "follow_source"
            def cond(r):
                sl, sr = r.detector.get_distance(1)
                return sl < 50 and sr < 50                                   # TODO FIND GOODENOUGH VALUES
            self.go_drive(pid_left, pid_right, tpser, avger, cond, 0)

        # run forward until IR contact
        def state_enter_source(self, pid_left, pid_right, tpser, avger):
            self.state = "enter_source"
            def cond(r):
                print(self.infraredSensor.proximity)
                return abs(self.infraredSensor.proximity - 3.5) <= 1           # TODO FIND GOODENOUGH VALUES
            self.go_drive(pid_left, pid_right, tpser, avger, cond, 1)
            self.drive.stop()

        # grab the cargo, do a 180
        def state_contact(self):
            self.state = "contact"
            self.claw.on_to_position(SpeedPercent(-10), -160)
            self.drive.rotate180()

        # seek end of the square
        def state_exit_source(self, pid_left, pid_right, tpser, avger):
            self.state = "exit_source"
            self.drive.short_sprint()

        # get out of source zone, seek crossroad
        def state_follow_source_2(self, pid_left, pid_right, tpser, avger):
            self.state = "follow_source_2"
            def cond(r):
                sl, sr = r.detector.get_distance(1)
                return sl < 100 or sr < 100                                    # TODO FIND GOODENOUGH VALUES
            self.go_drive(pid_left, pid_right, tpser, avger, cond, 0)

        # follow the line again until you find target color
        def state_seek_target(self, pid_left, pid_right, tpser, avger):
            self.state = "seek_target"
            def cond(r):
                sl, sr = r.detector.get_distance(2)
                return sl < 100 or sr < 100                                    # TODO FIND GOODENOUGH VALUES
            self.go_drive(pid_left, pid_right, tpser, avger, cond, 0)

        # follow the target color until square
        def state_follow_target(self, pid_left, pid_right, tpser, avger):
            self.state = "follow_target"
            def cond(r):
                sl, sr = r.detector.get_distance(2)
                return sl < 50 and sr < 50                                   # TODO FIND GOODENOUGH VALUES
            self.go_drive(pid_left, pid_right, tpser, avger, cond, 0)

        # run forward for some time
        def state_enter_target(self, pid_left, pid_right, tpser, avger):
            self.state = "enter_target"
            self.drive.last_sprint()

        # drop the cargo, done
        def state_drop(self):
            self.state = "drop"
            self.claw.on_to_position(SpeedPercent(-10), 0)

#######################################################################################

        def go_drive(self, pid_left, pid_right, tpser, avger, condition, color, color2=0):
            while True:
                tick = time()
                if condition(self): return self.detector.get_distance(color2)
                # Reading color sensors
                el, er = self.detector.get_distance(color)
                # Pid and steering control
                angle_left = pid_left.next(tick, 0, el) / 7
                angle_right = pid_right.next(tick, 0, er) / 7
                val_left = max(min(angle_left, 100), -100) / 5 # clamp to [-100, 100] and scale to [-20, 20]
                val_right = max(min(angle_right, 100), -100) / 5 # clamp to [-100, 100] and scale to [-20, 20]
                # Driving
                self.drive.correct(val_left, val_right)
                # Diagnostics
                tps_ = tpser.send(tick) # type: ignore
                self.print_all(el, er, val_left, val_right, tps_, avger.send(tps_))

        def print_init(self):
            self.printer.print_layout()
            self.printer.print_args(args)

        def print_all(self, el, er, val_left, val_right, tps_, avg_):
            self.printer.print_rawcolor(self.detector.left.rgb, self.detector.right.rgb)
            self.printer.print_errors(el, er)
            self.printer.print_vals(val_left, val_right)
            self.printer.print_action_move(val_left, val_right)
            self.printer.print_time(tps_, avg_)
            self.printer.print_state(self.state)

    def go_forth(robot):
        try:
            if robot.mode == "black":
                robot.main_black()
            elif robot.mode == "color":
                robot.main_color()
        except Exception as e:
            robot.drive.stop()
            robot.claw.on_to_position(SpeedPercent(-10), 0)
            robot.claw.off()
            r.printer.jump_prompt()
            raise e
        robot.drive.stop()
        robot.claw.on_to_position(SpeedPercent(-10), 0)
        robot.claw.off()
        r.printer.jump_prompt()

#######################################################################################

    # main body starts here
    signal.signal(signal.SIGINT, signal_handler)
    r = Robot()
    r.get_args(args)

    drive = Drive(OUTPUT_A, OUTPUT_D, r.defspeed, r.turnmod, r.turnflat)
    drive.stop()
    detector = Detector(INPUT_4, INPUT_1)
    #button = TouchSensor(INPUT_3)
    button = None
    r.register_devices(drive, detector, button, Printer())
    r.calibrate_colors()
    r.printer.print_action("\u001b[31mSTART ROBOT ?\u001b[0m")
    input()

    go_forth(r)
