#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_D

steer_pair = MoveTank(OUTPUT_D, OUTPUT_A, motor_class=LargeMotor)

def dead_reckoning(matrix):
    for row in matrix:
        left, right, time = row
        steer_pair.on_for_seconds(left, right, seconds=time)

command = [
  	[ 80, 60, 2],
  	[ 60, 60, 1],
  	[-50, 80, 2]
]
dead_reckoning(command)
