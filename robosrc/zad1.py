#!/usr/bin/ micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4
from time import sleep
import sys
import signal

from detector import Detector
from drive import Drive


def pprint(str, row=1, col=1, end='\n'):
    print("\033[{row};{col}H".format(row=row,col=col))
    print(str, end=end)

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

    def parse_args(self):
        self.light_threshold = int(sys.argv[1])
        self.normal_speed = int(sys.argv[2])
        self.slow_speed = int(sys.argv[3])
        self.high_speed = int(sys.argv[4])
        self.rot_speed = float(sys.argv[5])

    def main(self, drive, detector):
        #tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

        while True:
            light_left = detector.left()
            light_right = detector.right()

            txt = "{s1:.2f}, {s2:.2f}"
            pprint(txt.format(s1=light_left, s2=light_right), 3)

            if light_left < self.light_threshold and light_right < self.light_threshold:
                drive.move_forward()
                pprint("FORWARD BLACK", 2)
            elif light_left >= self.light_threshold and light_right >= self.light_threshold:
                drive.move_forward()
                pprint("FORWARD WHITE", 2)
            elif light_left < self.light_threshold and light_right >= self.light_threshold:
                drive.move_turn_left()
                pprint("TURN LEFT    ", 2)
            elif light_left >= self.light_threshold and light_right < self.light_threshold:
                drive.move_turn_right()
                pprint("TURN RIGHT   ", 2)

        #tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 3)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    print('OK JAZDA')
    r = Robot()
    if (len(sys.argv) > 1):
        r.parse_args()
    pprint("lo:{a} med:{b} hi:{c} rot:{d}".format(a=r.slow_speed, b=r.normal_speed, c=r.high_speed, d=r.rot_speed), 1)
    drive = Drive(OUTPUT_A, OUTPUT_D, r.slow_speed, r.normal_speed, r.high_speed, r.rot_speed)
    detector = Detector(INPUT_1, INPUT_4)
    r.main(drive, detector)
