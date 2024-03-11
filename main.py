#! /usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor, TouchSensor, GyroSensor
from pybricks.parameters import Port,Direction, Stop
from pybricks.tools import wait


motor_front = Motor(
    Port.B, gears=[8, 40], positive_direction=Direction.COUNTERCLOCKWISE
)
motor_back = Motor(Port.A, gears=[[12, 20], [8, 24]])
motor_lift = Motor(
    Port.D, positive_direction=Direction.COUNTERCLOCKWISE, gears=[8, 24, 40]
)

# The total degrees of rotation from the top of the lift to the bottom.
MOTOR_LIFT_HEIGHT = const(500)

sensor_gryo = GyroSensor(Port.S2, Direction.COUNTERCLOCKWISE)
sensor_lift = TouchSensor(Port.S3)

# The angle of the gyro sensor when the robot is maxmially tilted.
MAX_GRYO_ANGLE = const(45)


def calibrate():
    # TODO: jaguilar - Run to the sensor, then calculuate the position of 0 height instead of
    # using RunUntilStalled.
    if not sensor_lift.pressed():
        motor_lift.dc(50)
        while not sensor_lift.pressed():
            wait(3)
        motor_lift.stop()

    # We're at the top of the range of the lift. Now we need to run it downward. to the bottom.
    motor_lift.run_angle(100, -MOTOR_LIFT_HEIGHT)
    motor_lift.hold()
    motor_lift.reset_angle(0)
    sensor_gryo.reset_angle(0)


# Rear wheel diameter: 9 units.
# Circumference:            pi * 9 [diameter] = 28.3.
# Units/deg:                360 / 28.3 [cir] = 12.7
WHEEL_FRONT_DEG_PER_UNIT = 12.7


# Rear wheel diameter: 7 units.
# Circumference:            pi * 7 [diameter] = 22.0.
# Units/deg:                360 / 22.0 [cir] = 16.4
WHEEL_REAR_DEG_PER_UNIT = 16.4


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


def main():
    calibrate()

    # TODO: jaguilar - observed the motors "running until stalled" in action. They
    # don't actually stall. They cause the robot to start tilting backwards.
    # Plan:
    # * Run the motors more slowly.
    # * The moment backwards tilt is detected, stop.
    # * Reverse slowly until no backward tilt.
    # * Raise the crane, and run the front motor slowly forward.
    # * Run rear motor with light duty cycle? 5-10%?
    # * When forward tilt is detected, we're on the next stair.
    # * Then, we'll need to roll forward until we have two wheel contact on the front.
    #   This should be a fixed distance every time.
    # * After two wheels are on the next step, raise the crane.
    # * Return to start.

    wait(1000)

if __name__ == '__main__':
    main()
