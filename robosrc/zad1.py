#!/usr/bin/env micropython
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep
import sys
import signal

mA = LargeMotor(OUTPUT_A)
mD = LargeMotor(OUTPUT_D)

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    mA.on(speed=0)
    mD.on(speed=0)
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    #tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    

    color_sensor1 = ColorSensor(INPUT_1) 
    color_sensor4 = ColorSensor(INPUT_4)

    light_intensity_threshold = int(sys.argv[1])
    normal_speed = int(sys.argv[2])
    slow_speed = int(sys.argv[3])
    high_speed = int(sys.argv[4])

    while True:
        color_sensor1_reflected_light_intensity = color_sensor1.reflected_light_intensity
        color_sensor4_reflected_light_intensity = color_sensor4.reflected_light_intensity

        txt = "{s1:.2f}, {s2:.2f}"
        print(txt.format(s1=color_sensor1_reflected_light_intensity, s2=color_sensor4_reflected_light_intensity))

        if color_sensor1_reflected_light_intensity < light_intensity_threshold and color_sensor4_reflected_light_intensity < light_intensity_threshold:
            mA.on(speed=normal_speed)
            mD.on(speed=normal_speed)
            print(1)
        elif color_sensor1_reflected_light_intensity >= light_intensity_threshold and color_sensor4_reflected_light_intensity >= light_intensity_threshold:
            mA.on(speed=normal_speed)
            mD.on(speed=normal_speed) 
            print(2)
        elif color_sensor1_reflected_light_intensity < light_intensity_threshold and color_sensor4_reflected_light_intensity >= light_intensity_threshold:
            mA.on(speed=slow_speed)
            mD.on(speed=high_speed)
            print(3)
        elif color_sensor1_reflected_light_intensity >= light_intensity_threshold and color_sensor4_reflected_light_intensity < light_intensity_threshold:
            mA.on(speed=high_speed)
            mD.on(speed=slow_speed)
            print(4)
        sleep(0.1)

    #tank_drive.on_for_seconds(SpeedPercent(10), SpeedPercent(10), 3)


if __name__ == '__main__':
    main()
