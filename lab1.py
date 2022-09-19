#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_A, OUTPUT_D, MoveTank
from time import sleep
import sys

steer_pair = MoveSteering(OUTPUT_D, OUTPUT_A, motor_class=LargeMotor)
tank = MoveTank(OUTPUT_D, OUTPUT_A, motor_class=LargeMotor)

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
    debug_print('half circle')
    steer_pair.on_for_seconds(steering=25, speed=30, seconds=4)
    debug_print('straight')
    steer_pair.on_for_seconds(steering=0, speed=30, seconds=2)
    debug_print('straightening')
    steer_pair.on_for_seconds(steering=-90, speed=10, seconds=1)
    debug_print('half circle')
    steer_pair.on_for_seconds(steering=-25, speed=30, seconds=4)
    debug_print('returning to start')
    steer_pair.on_for_seconds(steering=0, speed=30, seconds=4)
    # steer_pair.on_for_seconds(steering=50, speed=30, seconds=1)
    # max_steer = 20
    # num_steps = 10
    # for step in range(num_steps):
    #     steer_pair.on(steering=step * max_steer / num_steps, speed=30)
    #     sleep(0.5)

def turn_90_degrees():
    steer_pair.on_for_seconds(steering=84, speed=10, seconds=1.6)
    # tank.on_for_seconds(36, -36, 0.25)

def rectangle():
    for step in range(4):
        debug_print('step {}'.format(step))
        steer_pair.on_for_seconds(steering=0, speed=30, seconds=1.5)
        turn_90_degrees()

rectangle()
# lemniscate()
# steer_pair.on_for_seconds(steering=90, speed=50, seconds=10, block=True)
# turn_90_degrees()
