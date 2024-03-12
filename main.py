#! /usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, GyroSensor
from pybricks.parameters import Port, Direction, Stop, Button
from pybricks.tools import wait, DataLog, StopWatch
import math
import time

brick = EV3Brick()

motor_front = Motor(
    Port.B, gears=[8, 40], positive_direction=Direction.COUNTERCLOCKWISE
)
motor_back = Motor(Port.A, gears=[[12, 20], [8, 24]])
motor_lift = Motor(
    Port.D, positive_direction=Direction.COUNTERCLOCKWISE, gears=[8, 24, 40]
)

# The total degrees of rotation from the top of the lift to the bottom.
MOTOR_LIFT_HEIGHT = const(500)


# Rear wheel diameter: 9 units.
# Circumference:            pi * 9 [diameter] = 28.3.
# Units/deg:                360 / 28.3 [cir] = 12.7
WHEEL_FRONT_DEG_PER_UNIT = 12.7


# Rear wheel diameter: 7 units.
# Circumference:            pi * 7 [diameter] = 22.0.
# Units/deg:                360 / 22.0 [cir] = 16.4
WHEEL_REAR_DEG_PER_UNIT = 16.4


# Lift track gear diameter: 5 units. Track piece is approx 1 unit thick.
# Circumference:            pi * 6 [dia + track] = 18.8.
# Units/deg:                360 / 18.8 [cir] = 19.1
LIFT_DEG_PER_UNIT = 19.1

sensor_gryo = GyroSensor(Port.S2, Direction.COUNTERCLOCKWISE)
sensor_lift = TouchSensor(Port.S3)

# The angle of the gyro sensor when the robot is maxmially tilted.
MAX_GRYO_ANGLE = const(45)


def calibrate():
    # TODO: jaguilar - Run to the sensor, then calculuate the position of 0 height instead of
    # using RunUntilStalled.
    if not sensor_lift.pressed():
        motor_lift.dc(50)
        motor_back.run(-0.5 * WHEEL_REAR_DEG_PER_UNIT)
        while not sensor_lift.pressed():
            wait(3)
        motor_lift.stop()
        motor_back.stop()

    # We're at the top of the range of the lift. Now we need to run it downward. to the bottom.
    motor_back.run(0.5 * WHEEL_REAR_DEG_PER_UNIT)
    motor_lift.run_angle(100, -MOTOR_LIFT_HEIGHT)
    motor_back.brake()
    motor_lift.hold()
    motor_lift.reset_angle(0)
    sensor_gryo.reset_angle(0)


# Note when we talk of units here we're talking of lego units on the lego grid.
def motors_run(speed_units_sec):
    motor_front.run(speed_units_sec * WHEEL_FRONT_DEG_PER_UNIT)
    motor_back.run(speed_units_sec * WHEEL_REAR_DEG_PER_UNIT)


def motors_run_until_stalled(speed_units_sec):
    # Run the front motor until stalled. We'll run the rear motor at the same speed to prevent drag, then stop it.
    motor_back.run(speed_units_sec * WHEEL_REAR_DEG_PER_UNIT)
    motor_front.run_until_stalled(speed_units_sec * WHEEL_FRONT_DEG_PER_UNIT)


def motors_brake():
    motor_front.brake()
    motor_back.brake()


def motors_hold():
    motor_front.hold()
    motor_back.hold()


def main():
    calibrate()

    while Button.CENTER not in brick.buttons.pressed():
        wait(10)
    brick.speaker.beep()
    wait(1000)

    # Run the motors forward until the gyro is off by more than 5 degrees.
    motors_run(7)
    while math.fabs(sensor_gryo.angle()) < 10:
        wait(10)

    motors_run(3)

    brick.speaker.beep()
    wait(1000)

    # Run the lift to its max height. Don't wait though.
    motor_lift.run_target(7 * LIFT_DEG_PER_UNIT, MOTOR_LIFT_HEIGHT, wait=False)

    while sensor_gryo.angle() < 3 and not sensor_lift.pressed():
        wait(10)
    motor_lift.stop()

    wait(2500)

    motors_run(7)
    motor_lift.run_target(10 * LIFT_DEG_PER_UNIT, 0, wait=True)
    wait(2500)
    motors_brake()

if __name__ == '__main__':
    main()
