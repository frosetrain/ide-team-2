"""This is the code for IDE Team 2!!!!"""

# FIXME: Remove unavailable imports and logging on SPIKE Prime

from csv import DictReader
from logging import FileHandler
from os import system
from typing import Optional

import colorlog

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Colors, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase

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

c_sensor.detectable_colors(
    (Color.RED, Color.YELLOW, Color.GREEN, Color.BLUE, Color.BLACK, Color.NONE)
)


class Turn:
    """A turning instruction."""

    def __init__(
        self,
        angle: int,
        speed: Optional[int] = None,
        begin_straight: Optional[bool] = False,
    ):
        """
        Initialize the turn.

        Args:
            angle (int): The angle of the turn. Can be set to zero.
            speed (Optional[int]): How fast the robot should line-track once it completes the turn.
                                   If not specified, the robot continues at its previous speed.
            begin_straight (Optional[bool]): Whether this turn precedes a straight.
        """
        self.angle = angle
        self.speed = speed
        self.begin_straight = begin_straight


# These are instructions for the robot to follow, in an array of Turn objects.
# Parameters are angle, speed, begin_straight.
# Straights mean that there is a 90-degree turn in the middle of the straight
TURNS: list[Turn] = [
    Turn(0, 240),  # 0, starting with normal speed
    Turn(90),  # 1
    Turn(-90),  # 2
    Turn(45, 150),  # 3, slow speed
    Turn(0),  # 4
    Turn(0),  # 5
    Turn(90),  # 6
    Turn(0),  # 7
    Turn(0),  # 8
    Turn(45, 240, True),  # 9, back to normal speed and start straight
    Turn(90),  # 10, funny right turn
    Turn(0),  # 11
    Turn(90),  # 12
    Turn(45, 150),  # 13, back to slow
    Turn(0),  # 14
    Turn(0),  # 15
    Turn(90),  # 16
    Turn(0),  # 17
    Turn(0),  # 18
    Turn(45, 300),  # 19, enter high speed and zoom to the other side of the map
    Turn(45, 150),  # 20, activate slow mode
    Turn(0),  # 21
    Turn(90),  # 22
    Turn(0),  # 23
    Turn(45, 240, True),  # 24, speed up and start second straight
    Turn(90),  # 25, funny right turn
    Turn(0),  # 26
    Turn(90),  # 27
    Turn(45, 150),  # 28, enter final slow zone
    Turn(0),  # 29
    Turn(90),  # 30
    Turn(0),  # 31
    Turn(45, 300),  # 32, yay we're done
]

# List of turns where cubes can be deposited
DEPOSITS = {21: "GREEN", 23: "RED", 29: "BLUE", 31: "YELLOW"}
DEPOSITS[4] = "RED"

# FIXME: test reading
instructions = open("cases.csv", "r")
reader = DictReader(instructions)
testcases = []
for row in reader:
    testcases.append(row)
caseid = 0
# FIXME:

# Storing where each cube is in the sorter
sort_slots = {
    "RED": 1,
    "YELLOW": 3,
    "GREEN": 2,
    "BLUE": 0,
}
current_slot = 0  # The currently open sort-slot
turn_number = 0  # This variable was previously called i
straight_count = 0  # Counting how long we are on a straight
on_straight = False  # Whether we are on a straight
colored_floor_count = (
    0  # Counting how long we are on a colored area without encountering a cube
)
speed = 240  # The speed of the robot

sort_motor.run_target(100, -15)

while True:
    # FIXME: test injection begins here
    try:
        case = testcases[caseid]
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

    # l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    # r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    # l_col = l_sensor.color()
    # r_col = r_sensor.color()
    # c_col = c_sensor.color()
    # FIXME:

    if sort_motor.angle() < 0 or sort_motor.angle() > 359:
        sort_motor.reset_angle(sort_motor.angle() % 360)

    funny_turn = l_co > 0.6 and r_co < 0.08 and on_straight and straight_count > 1000
    if funny_turn:
        logger.debug("funny right turn!?!?!? ")
        on_straight = False
        straight_count = 0

    # Detecting turns (including funny ones)
    if l_co + r_co < 0.24 or funny_turn:
        turn = TURNS[turn_number]
        # FIXME: hub.display.number(i)

        if turn.angle != 0:  # A real turn
            logger.info("turning... " + str(turn_number))
            db.stop()
            db.turn(turn.angle)
        else:  # Continue straight
            db.straight(10, then=Stop.NONE)
            logger.info("unturn... " + str(turn_number))

        if turn.speed is not None:  # If a new speed is specified
            speed = turn.speed
            db.settings(straight_speed=speed)
            logger.debug(f"new speed {speed}")

        if turn.begin_straight:
            logger.debug("start the straight")
            straight_count = 0
            on_straight = True

        if turn_number in DEPOSITS.keys():  # If a cube should be deposited here
            logger.info("Deposit")
            db.straight(100)
            db.turn(180)
            angle_difference = (
                sort_slots[DEPOSITS[turn_number]] * 90 - sort_motor.angle() + 10
            )
            if angle_difference < 0:
                rotation = angle_difference + 360
            else:
                rotation = angle_difference
            sort_motor.run_angle(100, angle_difference)
            db.straight(75)
            sort_motor.run_angle(100, 40)
            sort_slots[DEPOSITS[turn_number]] = -1

        turn_number += 1
        caseid += 1  # FIXME: remove test cases
        continue  # we go back to the top of while True to get new sensor values

    # Handling cases where there are no cubes on a colored floor
    if (
        l_col != Color.NONE
        and l_col != Color.WHITE
        and r_col != Color.NONE
        and r_col != Color.WHITE
    ):
        colored_floor_count += 1
    else:
        colored_floor_count = 0

    if colored_floor_count >= 80 and turn_number > 1:
        colored_floor_count = 0
        db.turn(180)
        db.straight(50)
        turn_number += 0

    # Line tracking
    sensi = 0.69
    if speed >= 240:
        sensi = 0.5
    # logger.debug(sensi)
    db.drive(speed, (l_co - r_co) * speed * sensi)

    # Incrementing straight_count if needed
    if on_straight:
        straight_count += 1
        # logger.debug(straight)

    # Picking up cubes if we see any
    # TODO: Only pick up cubes if it's in a valid position
    # FIXME: color = str(c_col)[6:]
    color = c_col
    if color in ["RED", "YELLOW", "GREEN", "BLUE"]:
        db.stop()
        db.straight(-10)
        db.turn(180)
        logger.info("Pick up")
        sort_motor.run_angle(250, 40)
        db.straight(-155)
        sort_motor.run_angle(250, 50)
        sort_slots[color] = current_slot
        current_slot += 1

    caseid += 1
