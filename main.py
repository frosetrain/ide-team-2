"""This is the code for IDE Team 2!!!!"""

from csv import DictReader

from os import system

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Colors, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase

import colorlog
from logging import FileHandler

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s%(message)s"))
filehandle = FileHandler("first.log")

logger = colorlog.getLogger(__name__)
logger.setLevel("DEBUG")
logger.addHandler(handler)
logger.addHandler(filehandle)


system("clear")

L_CO_BLACK = 12
R_CO_BLACK = 12
L_CO_WHITE = 89
R_CO_WHITE = 82

TURNS = [
    0,  # 0
    90,  # 1
    -90,  # 2
    45,  # 3
    0,  # 4
    0,  # 5
    90,  # 6
    0,  # 7
    0,  # 8
    45,  # 9
    90,  # 10
    0,  # 11
    90,  # 12
    45,  # 13
    0,  # 14
    0,  # 15
    90,  # 16
    0,  # 17
    0,  # 18
    45,  # 19
    45,  # 20
    0,  # 21
    # 0,
    90,  # 22
    0,  # 23
    # 0,
    45,  # 24
    90,  # 25
    0,  # 26
    90,  # 27
    45,  # 28
    0,  # 29
    # 0,
    90,  # 30
    0,  # 31
    # 0,
    45,  # 32
]


# Hardware definitions
hub = PrimeHub()
left_motor = Motor(
    Port.E, positive_direction=Direction.COUNTERCLOCKWISE, gears=None, reset_angle=True
)
right_motor = Motor(
    Port.A, positive_direction=Direction.CLOCKWISE, gears=None, reset_angle=True
)
sort_motor = Motor(
    Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=None, reset_angle=True
)
l_sensor = ColorSensor(Port.F)
r_sensor = ColorSensor(Port.B)
c_sensor = ColorSensor(Port.D)
db = DriveBase(left_motor, right_motor, 88, 207)
db.settings(straight_speed=200)

c_sensor.detectable_colors(
    (Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.BLACK, Color.NONE)
)


def pick_up() -> None:
    """Pick up a cube from a colored area."""
    logger.info("Pick up")
    # hub.speaker.beep(frequency=523.2, duration=200)
    sort_motor.run_angle(250, 40)
    db.straight(-155)
    sort_motor.run_angle(250, 50)


def abort() -> None:
    about_turn()
    db.straight(50)


def deposit(col) -> None:
    """Raise the sort, move backwards, then lower the sort."""
    logger.info("Deposit")
    db.straight(100)
    about_turn()
    # db.straight(-50)
    sort_motor.run_angle(
        100, clock_angle((colors[col] * 90 + 10) - (sort_motor.angle()))
    )
    db.straight(75)
    sort_motor.run_angle(100, 40)
    colors[col] = -1


def drive(x, l_co, r_co) -> None:
    """Do some line tracking."""
    sensi = 0.69
    # l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    # r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    # db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 275)
    if power:
        sensi = 0.5
    # logger.debug(sensi)
    db.drive(x, (l_co - r_co) * x * sensi)


def about_turn() -> None:
    """Turn around 180 degrees."""
    db.turn(180)


def clock_angle(x):
    if x < 0:
        # logger.debug(360 + x)
        return 360 + x
    else:
        # logger.debug(x)
        return x


if __name__ == "__main__":
    seq = open("cases.csv", "r")
    reader = DictReader(seq)
    cases = []
    for row in reader:
        cases.append(row)
    caseid = 0

    colors = {"RED": 1, "YELLOW": 3, "GREEN": 2, "BLUE": 0}
    curr_angle = 0
    i = 0
    speed = 230
    straight = 0
    turned = 0
    ons = False
    onPower = 250
    power = True
    diff_color = 0
    sort_motor.run_target(100, -15)

    while False:
        # l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
        # r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
        logger.debug(l_sensor.reflection(), r_sensor.reflection())
    while True:
        try:
            case = cases[caseid]
        except IndexError:
            logger.debug("done")
            exit()
        logger.info(case)
        l_co = float(case["l_ref"])
        r_co = float(case["r_ref"])
        l_col = Colors[case["l_col"]]
        r_col = Colors[case["r_col"]]
        c_col = case["c_col"]
        # logger.debug(l_co, r_co, l_col, r_col, c_col)

        if sort_motor.angle() < 0 or sort_motor.angle() > 359:
            sort_motor.reset_angle(sort_motor.angle() % 360)

        # l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
        # r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
        # l_col = l_sensor.color()
        # r_col = r_sensor.color()
        # c_col = c_sensor.color()
        # FIXME

        if (
            l_col != Color.NONE
            and l_col != Color.WHITE
            and r_col != Color.NONE
            and r_col != Color.WHITE
        ):
            diff_color += 1
        else:
            diff_color = 0

        if diff_color >= 80 and i > 1:
            diff_color = 0
            abort()
            i += 0

        # logger.debug(diff_color)

        if l_co > 0.6 and r_co < 0.08 and ons and straight > 1000:
            # We can merge this with the If below
            logger.debug("funny right turn!?!?!? ")
            onPower = 0
            speed = 200
            db.straight(50, then=Stop.NONE)
            db.turn(TURNS[i])
            # db.turn(90)
            ons = False
            straight = 0
            i += 1

        if l_co + r_co < 0.24:
            if power:
                onPower = 0
                speed = 250
            # hub.display.number(i)
            # FIXME
            # hub.speaker.beep(frequency=493.8+(30*i), duration=10)
            if i == 4:
                db.straight(10, then=Stop.NONE)
            else:
                db.straight(45, then=Stop.NONE)

            if TURNS[i] != 0:
                # db.straight(15, then=Stop.NONE)
                logger.info("turning... " + str(i))
                db.stop()
                db.turn(TURNS[i])
                # db.turn(90)
            else:
                db.straight(5, then=Stop.NONE)
                logger.info("unturn... " + str(i))

            if (
                (i >= 3 and i <= 8)
                or (i >= 13 and i <= 18)
                or (i >= 20 and i <= 23)
                or (i >= 28 and i <= 31)
            ):
                logger.debug("slow")
                onPower = 0
                speed = 150
                power = False
            else:
                logger.debug("speed")
                power = True

            if i == 9 or i == 24:
                # db.straight(15, then=Stop.NONE)
                logger.debug("start the straight")
                straight = 0
                ons = True
            # elif i == 10 or i == 11 or i == 19 or i == 26 or i == 27:
            # speed = 180
            # else:
            # speed = 180

            if i == 21:
                deposit("GREEN")
            if i == 23:
                deposit("RED")
            if i == 29:
                deposit("BLUE")
            if i == 31:
                deposit("YELLOW")
            i += 1
        if power:
            onPower += 1
            if onPower > 400 and speed < 375:
                speed += 0.4
        # logger.debug(speed, onPower)
        # hub.speaker.beep(frequency=(speed)*5-500, duration=10)
        drive(speed, l_co, r_co)

        if ons:
            straight += 1
            # logger.debug(straight)

        # color = str(c_col)[6:]
        color = c_col
        # logger.debug(color)
        if color in ["RED", "YELLOW", "GREEN", "BLUE"]:
            db.stop()
            db.straight(-10)
            about_turn()
            pick_up()
            colors[color] = curr_angle
            curr_angle += 1

        caseid += 1
