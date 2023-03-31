"""This is the code for IDE Team 2!!!!"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

left_motor = Motor(
    Port.F, positive_direction=Direction.CLOCKWISE, gears=None, reset_angle=True
)
right_motor = Motor(
    Port.D, positive_direction=Direction.COUNTERCLOCKWISE, gears=None, reset_angle=True
)
claw_motor = Motor(
    Port.B, positive_direction=Direction.CLOCKWISE, gears=None, reset_angle=True
)

l_sensor = ColorSensor(Port.A)
r_sensor = ColorSensor(Port.E)

c_sensor = ColorSensor(Port.C)

db = DriveBase(left_motor, right_motor, 88, 165)


def get_sensor_values() -> None:
    """Get the light sensor values. Used for debugging."""
    l_ref = l_sensor.reflection()
    r_ref = r_sensor.reflection()
    l_hsv = l_sensor.hsv()
    r_hsv = l_sensor.hsv()
    l_col = l_sensor.color()
    r_col = r_sensor.color()
    c_col = c_sensor.color()
    print(l_ref, r_ref, l_hsv.h, l_hsv.s, l_hsv.v, r_co, r_hsv.h, r_hsv.s, r_hsv.v)
    # wait(50)
    # MAX: 62, 66
    # MIN: 7, 8


def pick_up() -> None:
    """Raise the claw, move backwards, then lower the claw."""
    claw_motor.run_angle(250, 90)
    db.straight(100)
    claw_motor.run_angle(250, -90)


def deposit() -> None:
    """Raise the claw, move backwards, then lower the claw."""
    db.straight(50)
    claw_motor.run_angle(250, 90)
    db.straight(-100)
    claw_motor.run_angle(250, -90)


def drive() -> None:
    """Do some line tracking."""
    l_co = (l_sensor.reflection() - 7) / 55
    r_co = (r_sensor.reflection() - 8) / 58
    # db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 275)
    db.drive(200, (l_co - r_co) * 100)
    # 350, 250
    # Ratio of 7:5""


def about_turn() -> None:
    """Turn around 180 degrees."""
    db.turn(180)


if __name__ == "__main__":
    while True:
        drive()
        l_ref = l_sensor.reflection()
        r_ref = r_sensor.reflection()
        l_hsv = l_sensor.hsv()
        r_hsv = l_sensor.hsv()
        l_col = l_sensor.color()
        r_col = r_sensor.color()
        c_col = c_sensor.color()
        print(l_ref, r_ref, l_col, l_hsv.h, l_hsv.s, l_hsv.v, r_col, r_hsv.h, r_hsv.s, r_hsv.v)
        if l_col == Color.BLUE and r_col == Color.BLUE:
            deposit()
            about_turn()
        if c_col == Color.RED:
            db.stop()
            # db.straight(-10)
            pick_up()
