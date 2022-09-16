#!/usr/bin/env python3
from sqlite3 import DateFromTicks
from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import GyroSensor
from time import sleep
import sys
import math

steer_pair = MoveTank(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
gyro = GyroSensor()
motor = steer_pair.left_motor


command = [
  	[ 50, 30, 2],
  	# [ 60, 40, 1],
  	# [-50, 80, 2]
]
print('tachos per rotation: ', steer_pair.left_motor.count_per_rot, file=sys.stderr)
print('Starting angle: ', gyro.angle, file=sys.stderr)


def get_forward_velocity():
    return 0


def wheel_speeds():
    wheel_diameter = 0.057
    wheel_circumference = wheel_diameter * math.pi
    v_left = steer_pair.left_motor.speed / 360 * wheel_circumference
    v_right = steer_pair.right_motor.speed / 360 * wheel_circumference
    return v_left, v_right

def radius_of_curvature():
    wheel_distance = 0.108
    v_left, v_right = wheel_speeds()
    if math.isclose(v_left, v_right, abs_tol=0.0001):
        return float('inf')
    return wheel_distance * (v_left + v_right) / (v_right - v_left)

def straight():
    drive_time = 5
    steer_pair.on_for_seconds(30, 30, seconds=drive_time, block=False)
    speeds = []
    for i in range(10):
        speeds.append(wheel_speeds())
        sleep(drive_time/10)

    wheel_diameter = 0.057
    wheel_circumference = wheel_diameter * math.pi
    print(speeds, sep='\n', file=sys.stderr)
    v_left_avg = sum([x[0] for x in speeds]) / len(speeds)
    v_right_avg = sum([x[1] for x in speeds]) / len(speeds)
    print('Average left speed', v_left_avg, file=sys.stderr)
    print('Average right speed', v_right_avg, file=sys.stderr)
    print('Final distance travelled', steer_pair.left_motor.position / 360 * wheel_circumference, file=sys.stderr)
    print('Ending Angle: {} ({})'.format(gyro.angle, gyro.angle % 360), file=sys.stderr)

def dead_reckoning(matrix):
    x = y = 0
    theta = gyro.angle
    for row in matrix:
        left, right, time = row
        steer_pair.on_for_seconds(left, right, seconds=time, block=False)
        sleep(time/2)
        R = radius_of_curvature()
        v_left, v_right = wheel_speeds()
        print('Wheel speeds: {:.3f},{:.3f}'.format(v_left, v_right), file=sys.stderr)
        sleep(time/2)
        delta = ((gyro.angle - theta) %360 )/ 180 * math.pi
        print('Delta theta {}, R: {}'.format(delta, R), file=sys.stderr)
        theta = gyro.angle
        v_avg = v_left + v_right / 2
        if R != float('inf'):
            x += math.cos(delta) * v_avg * time
            y += math.sin(delta) * v_avg * time
        else:
            x += v_avg * time
            y += v_avg * time
        print('Current location {:.3f}, {:.3f}'.format(x, y), file=sys.stderr)
        print('Ending Angle {:.3f}'.format(gyro.angle), file=sys.stderr)

dead_reckoning(command)
