"""This is the code for IDE Team 2!!!!"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

hub = PrimeHub()

left_motor = Motor(
    Port.F,
    positive_direction=Direction.COUNTERCLOCKWISE,
    gears=None,
    reset_angle=True
)
right_motor = Motor(
    Port.D,
    positive_direction=Direction.CLOCKWISE,
    gears=None,
    reset_angle=True
)
claw_motor = Motor(
    Port.B,
    positive_direction=Direction.CLOCKWISE,
    gears=None,
    reset_angle=True
)

l_sensor = ColorSensor(Port.E)
r_sensor = ColorSensor(Port.A)

c_sensor = ColorSensor(Port.C)

db = DriveBase(left_motor, right_motor, 88, 165)


def get_sensor_values() -> None:
    """Get the light sensor values. Used for debugging."""
    l_co = l_sensor.reflection()
    r_co = r_sensor.reflection()
    l_cl = l_sensor.color()
    r_cl = l_sensor.color()
    c_cl = c_sensor.color()
    print(l_cl, r_cl, c_cl)
    # wait(50)
    # MAX: 62, 66
    # MIN: 7, 8


def pick_up() -> None:
    """Raise the claw, move backwards, then lower the claw."""
    claw_motor.run_angle(250, 90)
    db.straight(-100)
    claw_motor.run_angle(250, -90)


def deposit() -> None:
    """Raise the claw, move forwards, then lower the claw."""
    claw_motor.run_angle(250, 90)
    db.straight(100)
    claw_motor.run_angle(250, -90)


def drive() -> None:
    """Do some line tracking."""
    l_co = (l_sensor.reflection() - 7) / 55
    r_co = (r_sensor.reflection() - 8) / 58
    # db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 275)
    db.drive(250, (l_co - r_co) * 150)
    # 350, 250
    # Ratio of 7:5""


def about_turn() -> None:
    """Turn around 180 degrees."""
    db.turn(180)


if __name__ == "__main__":
    while True:
        for i in range(5):
            drive()
        l_cl = l_sensor.color()
        r_cl = l_sensor.color()
        clc = c_sensor.color()
        print(l_cl, r_cl, clc)
        if l_cl == Color.BLUE and r_cl == Color.BLUE:
            about_turn()
            deposit()

        if clc == Color.RED:
            db.straight(-50)
            about_turn()
            pick_up()
            about_turn()
