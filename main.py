#! /usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor, TouchSensor, GyroSensor
from pybricks.parameters import Port,Direction, Stop
from pybricks.tools import wait

motor_front = Motor(Port.B)
motor_back = Motor(Port.A)
motor_lift = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)

sensor_gryo = GyroSensor(Port.S2)
sensor_lift = TouchSensor(Port.S3)


def calibrate():
    # TODO: jaguilar - Run to the sensor, then calculuate the position of 0 height instead of
    # using RunUntilStalled.
    motor_lift.run_until_stalled(-180, duty_limit=40, then=Stop.HOLD)
    motor_lift.reset_angle(0)
    motor_lift.run(180)
    while not sensor_lift.pressed():
        wait(5)
    motor_lift.stop()
    print("sensor_pressed")
    throw = motor_lift.angle()
    print(throw)
    motor_lift.run_angle(-720, 0, then=Stop.HOLD)
    wait(50)

def main():
    calibrate()

if __name__ == '__main__':
    main()
