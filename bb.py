#!/usr/bin/env python3
from ev3dev2.sensor import INPUT_2, INPUT_4
from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import ColorSensor, LightSensor
import ev3dev2
import sys
from time import sleep
from enum import Enum

class BBMode(Enum):
    AGGRESSION = 1
    FEAR = 2

steer_pair = MoveTank(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
light_sens_left = ColorSensor(INPUT_2)
light_sens_right = ColorSensor(INPUT_4)
light_sens_left.mode = ColorSensor.MODE_COL_AMBIENT
light_sens_right.mode = ColorSensor.MODE_COL_AMBIENT

mode = BBMode.FEAR
while True:
    left = light_sens_left.ambient_light_intensity
    right = light_sens_right.ambient_light_intensity
    left = min(2 *light_sens_left.ambient_light_intensity, 100)
    right = min(2 * light_sens_right.ambient_light_intensity, 100)
    print('Light intensity -- Left: {} Right: {}'.format(left, right), file=sys.stderr)
    if mode == BBMode.AGGRESSION:
        steer_pair.on(right, left)
    elif mode == BBMode.FEAR:
        steer_pair.on(left, right)
    sleep(0.2)
