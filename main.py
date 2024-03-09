#! /usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor, TouchSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait

motor_front = Motor(Port.B)
motor_back = Motor(Port.A)
motor_lift = Motor(Port.D)

sensor_gryo = GyroSensor(Port.S2)
sensor_lift_limit = TouchSensor(Port.S3)


def calibrate():

    
    pass
