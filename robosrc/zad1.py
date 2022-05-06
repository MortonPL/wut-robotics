#!/usr/bin/env micropython
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D
from ev3dev2.sensor import INPUT_1, INPUT_4
from time import sleep
import sys
import signal

from detector import Detector
from drive import Drive

# Globals zone
drive = Drive(OUTPUT_A, OUTPUT_D)
detector = Detector(INPUT_1, INPUT_4)
light_threshold = 0
normal_speed = 0
slow_speed = 0
high_speed = 0

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    drive.stop()
    sys.exit(0)

def parse_args():
    light_threshold = int(sys.argv[1])
    normal_speed = int(sys.argv[2])
    slow_speed = int(sys.argv[3])
    high_speed = int(sys.argv[4])

def main():
    #tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)

    while True:
        light_left = detector.left()
        light_right = detector.right()

        txt = "{s1:.2f}, {s2:.2f}"
        print(txt.format(light_left, light_right))

        if light_left < light_threshold and light_right < light_threshold:
            drive.move_forward()
            print("FORWARD BLACK")
        elif light_left >= light_threshold and light_right >= light_threshold:
            drive.move_forward()
            print("FORWARD WHITE")
        elif light_left < light_threshold and light_right >= light_threshold:
            drive.move_turn_left()
            print("TURN LEFT")
        elif light_left >= light_threshold and light_right < light_threshold:
            drive.move_turn_right()
            print("TURN RIGHT")
        sleep(0.1)

    #tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 3)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    parse_args()
    main()
