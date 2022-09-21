#!/usr/bin/env python3
from sqlite3 import DateFromTicks
from ev3dev2.motor import LargeMotor, MoveTank, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import GyroSensor
from time import sleep, time
import time
import sys
import math

steer_pair = MoveTank(OUTPUT_A, OUTPUT_D, motor_class=LargeMotor)
gyro = GyroSensor()
motor = steer_pair.left_motor


command = [
  	[ 20, 30, 2],
  	[ 40, 20, 4],
  	# [-50, 80, 2]
]
print('tachos per rotation: ', steer_pair.left_motor.count_per_rot, file=sys.stderr)

wheel_circumference = 0.221

def get_forward_velocity():
    return 0


def wheel_speeds():
    v_left = steer_pair.left_motor.speed / 360 * wheel_circumference
    v_right = steer_pair.right_motor.speed / 360 * wheel_circumference
    return v_left, v_right

def radius_of_curvature():
    wheel_distance = 0.12
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
    theta = 0
    wheel_distance = 0.115
    print('Starting angle: ', theta, file=sys.stderr)
    for row in matrix:
        left, right, time = row
        steer_pair.on_for_seconds(left, right, seconds=time, block=False)
        sleep(time/2)
        R = radius_of_curvature()
        v_left, v_right = wheel_speeds()
        omega = (v_right - v_left )/ wheel_distance
        delta_theta = omega * time
        theta += delta_theta
        print('Wheel speeds: {:.3f},{:.3f}'.format(v_left, v_right), file=sys.stderr)
        sleep(time/2)
        # print('Angle: {} Delta theta {:3f}, R: {}'.format(new_theta, delta, R), file=sys.stderr)
        # theta = gyro.angle
        v_avg = (v_left + v_right) / 2
        if R != float('inf'):
            x += math.cos(theta) * v_avg * time
            y += math.sin(theta) * v_avg * time
        else:
            x += v_avg * time * math.cos(theta )
            y += v_avg * time * math.sin(theta )
        print('v_left: {:.3f} v_right: {:.3f} v_avg: {:.3f}'.format(v_left, v_right, v_avg), file=sys.stderr)
        print('Current location {:.3f}, {:.3f} at {} degrees'.format(x, y, (theta / math.pi *  180)%360), file=sys.stderr)
        print('Angle from gyroscope = {:.3f}'.format(gyro.angle % 360), file=sys.stderr)

def dead_reckoning1(matrix):
    x = y = 0
    distance_travelled = 0
    print('Starting position:',steer_pair.left_motor.position, file=sys.stderr)
    for row in matrix:
        left, right, command_duration = row
        steer_pair.on_for_seconds(left, right, seconds=command_duration, block=False, brake = True)
        timestep = 0.05
        elapsed_time = 0
        while elapsed_time < command_duration:
            left_pos = steer_pair.left_motor.position
            right_pos = steer_pair.right_motor.position
            sleep(timestep / 2)
            theta = gyro.angle
            sleep(timestep/2)
            end_left = steer_pair.left_motor.position
            # print('Left motor delta tacho: {}-{}'.format(end_left, left_pos), file=sys.stderr)
            v_left = (  end_left - left_pos ) / 360 * wheel_circumference / timestep
            v_right =(  steer_pair.right_motor.position - right_pos ) / 360 * wheel_circumference / timestep
            v_avg = (v_left + v_right) / 2
            x += math.cos(theta / 180 * math.pi) * v_avg * timestep
            y += math.sin(theta / 180 * math.pi) * v_avg * timestep
            distance_travelled += v_avg * timestep
            elapsed_time += timestep
            d = steer_pair.left_motor.position / 360 * wheel_circumference
            # print('time = {:.1f} pos = ({:.3f},{:.3f}) angle={} - v_left: {:.3f} ({:.3f}) v_right: {:.3f} ({:.3f}) v_avg: {:.3f}'.format(elapsed_time, x, y, theta, v_left, steer_pair.left_motor.speed, v_right,steer_pair.right_motor.speed, v_avg), file=sys.stderr)
            # print('distance travelled {:.3f} ({} tachos) or {:.3f}'.format(d, steer_pair.left_motor.position, distance_travelled), file=sys.stderr)
            # print('--------------------------------', file=sys.stderr)
    print('time = {:.1f} pos = ({:.3f},{:.3f}) angle={}'.format(elapsed_time, x, y, theta), file=sys.stderr)
    print('Final distance travelled {:.3f} or {:.3f}'.format(d, distance_travelled), file=sys.stderr)

gyro.reset()
dead_reckoning(command)
# gyro.calibrate()
