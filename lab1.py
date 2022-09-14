#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor
from ev3dev2.motor import MoveSteering, OUTPUT_A, OUTPUT_D
from time import sleep
import sys

steer_pair = MoveSteering(OUTPUT_D, OUTPUT_A, motor_class=LargeMotor)

def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.

    This shows up in the output panel in VS Code.
    '''
    print(*args, **kwargs, file=sys.stderr)

# debug_print('Starting to drive straight')
# steer_pair.on_for_seconds(steering=0, speed=20, seconds=5, block=True)
# debug_print('Steering to the left')
# steer_pair.on_for_seconds(steering=-80, speed=20, seconds=5, block=True)
# debug_print('Starting to the right')
# steer_pair.on_for_seconds(steering=80, speed=20, seconds=5, block=True)

# def print_rotations():
#     rotations = lm.position / lm.count_per_rot
#     debug_print('Current rotations: {:.2f}'.format(rotations))


'''
This will run the large motor at 50% of its
rated maximum speed of 1050 deg/s.
50% x 1050 = 525 deg/s
'''

def lemniscate():
    debug_print('step 1')
    for step in range(10):
        steer_pair.on(steering=step * 2, speed=30)
        sleep(0.5)

    debug_print('step 2')
    sleep(15)
    debug_print('step 3')
    for step in range(10):
        steer_pair.on(steering=20 - step * 2, speed=30)
        sleep(0.5)
    debug_print('step 4')
    sleep(5)

    for step in range(10):
        steer_pair.on(steering=-step * 2, speed=30)
        sleep(0.5)

def rectangle():
    for step in range(4):
        debug_print('step {}'.format(step))
        steer_pair.on_for_seconds(steering=0, speed=30, seconds=5)
        steer_pair.on_for_seconds(steering=90, speed=30, seconds=1.55)
lemniscate()
# rectangle()
# steer_pair.on_for_seconds(steering=100, speed=50, seconds=10, block=True)
