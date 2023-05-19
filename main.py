"""This is the code for IDE Team 2!!!!"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch

watch = StopWatch()

L_CO_BLACK = 12
R_CO_BLACK = 12
L_CO_WHITE = 89
R_CO_WHITE = 89

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
db = DriveBase(left_motor, right_motor, 88, 213)

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
    Turn(-90, 500),  # 2
    Turn(45, 140),  # 3, slow speed
    Turn(0),  # 4
    Turn(90),  # 5
    # Turn(0),  # 6
    Turn(0),  # 6
    Turn(45, 500, True),  # 7, back to normal speed and start straight
    Turn(90, 499),  # 8, funny right turn
    Turn(0),  # 9
    Turn(90),  # 10
    Turn(45, 140),  # 11, back to slow
    # Turn(0),  # 12
    Turn(0),  # 12
    Turn(90),  # 13
    # Turn(0),  # 15
    Turn(0),  # 14
    Turn(45, 500),  # 15, enter high speed and zoom to the other side of the map
    Turn(45, 140),  # 16, activate slow mode
    Turn(0),  # 17
    Turn(90),  # 18
    Turn(0),  # 19
    Turn(45, 500, True),  # 20, speed up and start the second straight
    Turn(90, 499),  # 21, funny right turn
    Turn(0),  # 22
    Turn(90),  # 23
    Turn(45, 140),  # 24, enter final slow zone
    Turn(0),  # 25
    Turn(90),  # 26
    Turn(0),  # 27
    # Turn(45, 500),  # 28, yay we're done
]

# List of turns where cubes can be deposited
DEPOSITS = {17: "GREEN", 19: "RED", 25: "BLUE", 27: "YELLOW"}

# Storing where each cube is in the sorter
sort_slots = {
    "RED": -1,
    "YELLOW": 0,
    "GREEN": -1,
    "BLUE": -1,
}

occupied = {
    0: True,
    1: False,
    2: False,
    3: False,
}

BLUE_LIST: list[Turn] = [Turn(-90), Turn(0), Turn(-45, 500, True)]

RED_LIST: list[Turn] = [Turn(-45, 140), Turn(0)]

GREEN_LIST: list[Turn] = [Turn(0)]

current_slot = 1  # The currently open sort-slot
turn_number = 16  # This variable was previously called i
turn_frame = 0  # The frame where the robot last turned
on_straight = False  # Whether we are on a straight
last_non_white = "NONE"
remainder = False
colored_floor_count = (
    0  # Counting how long we are on a colored area without encountering a cube
)
speed = 240  # The speed of the robot
frame_id = 0  # How many times the while loop has run

# sort_motor.reset_angle()
sort_motor.run_target(100, 75)
print(sort_motor.angle())


def deposit():
    # db.straight(120)
    # db.turn(180)
    current_slot = sort_slots[last_non_white]
    print("WAS: ", sort_slots)
    print(current_slot)
    angle_difference = ((current_slot) * 90) - (sort_motor.angle()) + 10
    if angle_difference < 0:
        angle_difference += 360
        print(angle_difference)

    db.straight(-25)
    sort_motor.run_angle(200, angle_difference)

    # sort_motor.run_angle(200, angle_difference)

    db.straight(95)
    sort_motor.run_angle(200, 40)
    if sort_motor.angle() < 0 or sort_motor.angle() > 359:
        sort_motor.reset_angle(sort_motor.angle() % 360)

    # Reset to lowest slot:

    occupied[sort_slots[last_non_white]] = False
    sort_slots[last_non_white] = -1

    for slot in occupied:
        print("DEBUG:", slot)
        if not occupied[slot]:
            print("YES")
            current_slot = slot
            break
        else:
            print("NO")

    print("NEW SLOT:", current_slot)

    angle_difference = (current_slot * 90) - (sort_motor.angle())
    # print(angle_difference, sort_motor.angle())
    if angle_difference < 0:
        angle_difference += 360
        print(angle_difference)

    sort_motor.run_angle(200, angle_difference)

    print("NOW: ", sort_slots)
    print("NOW:", occupied)
    current_slot -= 1


while True:
    # print(current_slot)
    l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    l_col = l_sensor.color()
    r_col = r_sensor.color()
    c_col = c_sensor.color()
    hub.display.number(turn_number)

    # if on_straight:
    # print(l_co, r_co, l_col, r_col, c_col)

    if sort_motor.angle() < 0 or sort_motor.angle() > 359:
        sort_motor.reset_angle(sort_motor.angle() % 360)

    funny_turn = (
        ((l_co > 0.6 and r_co < 0.07) or (l_co < 0.07 and r_co > 0.6))
        and on_straight
        and frame_id - turn_frame > 500
    )

    if funny_turn:
        print("funny turn!?!?!? ")
        on_straight = False
        straight_count = 0

    # Detecting turns (including funny ones)
    if l_co + r_co < 0.1 or funny_turn:
        print("SLOT IS:", current_slot)
        turn = TURNS[turn_number]
        # hub.display.number(turn_number)
        turn_frame = frame_id
        print(turn_frame)

        if turn.angle != 0:  # A real turn
            # db.stop()
            # db.curve(50, turn.angle, then=Stop.COAST)

            db.straight(40, then=Stop.NONE)
            # print("turning... " + str(turn_number))
            db.stop()
            db.turn(turn.angle)
        else:  # Continue straight
            db.straight(25, then=Stop.NONE)
            # print("unturn... " + str(turn_number))

        if turn.speed is not None:  # If a new speed is specified
            speed = turn.speed
            db.settings(straight_speed=speed)
            # print(f"new speed {speed}")

        if turn.begin_straight:
            # print("start the straight")
            on_straight = True
        else:
            on_straight = False
        if turn_number == 20:
            print(sort_slots)
        # if turn_number in DEPOSITS.keys():  # If a cube should be deposited here
        # deposit()

        turn_number += 1
        continue  # we go back to the top of while True to get new sensor values

    # Handling cases where there are no cubes on a colored floor
    if (
        l_col != Color.NONE
        and l_col != Color.WHITE
        and r_col != Color.NONE
        and r_col != Color.WHITE
    ):
        colored_floor_count += 1
        last_non_white = str(l_col)[6:]
    else:
        colored_floor_count = 0

    if colored_floor_count >= 250 and turn_number > 1:
        colored_floor_count = 0
        db.turn(180)
        if turn_number > 16 and sort_slots[last_non_white] != -1:
            deposit()
            current_slot -= 1
        db.straight(50)

    # Picking up cubes if we see any
    # TODO: Only pick up cubes if it's in a valid position
    color = str(c_col)[6:]
    # color = c_col
    if color in ["RED", "YELLOW", "GREEN", "BLUE"]:
        if color == last_non_white:
            db.turn(178, wait=False)
        else:
            # db.stop()
            # db.straight(-10)
            db.turn(178, wait=False)
            print("Pick up")
            # current_slot -= 1
            print("WAS: ", current_slot)

            sort_motor.run_angle(200, 40)
            while not db.done():
                pass
            db.straight(-150)
            sort_motor.run_angle(200, 50)
            print(color)
            sort_slots[color] = current_slot
            occupied[current_slot] = True
            db.straight(150)

            current_slot = 0
            for slot in occupied:
                print("DEBUG:", slot)
                if not occupied[slot]:
                    print("YES")
                    current_slot = slot
                    break
                else:
                    print("NO")
                    current_slot += 1

            print("NEW SLOT:", current_slot)
            print("NOW: ", sort_slots)
            print("NOW:", occupied)

        if turn_number > 16 and sort_slots[last_non_white] != -1:
            deposit()

        continue

    if turn_number == 28 and remainder == False:
        print("NOW: ", sort_slots)
        if not (sort_slots["GREEN"] == -1):
            print("GREEEEEEEEEEN")
            TURNS = TURNS + BLUE_LIST
        else:
            print("no green L")
            TURNS += [Turn(45, 500, True)]

        TURNS += [Turn(-90, 499), Turn(0), Turn(-90)]

        if not (sort_slots["RED"] == -1):
            print("REDDDDDDDDDDD")
            TURNS = TURNS + RED_LIST
            if sort_slots["BLUE"] != 1:
                print("BLUE")
                TURNS += [Turn(-90, 140)]
                TURNS += [Turn(0)]
        if not (sort_slots["BLUE"] == -1):
            print("BLUE")
            TURNS += [Turn(45, 140)]
            TURNS += [Turn(0)]

        remainder = True

    # Line tracking
    if speed < 240:
        sensi = 0.69
    elif speed == 240:
        sensi = 0.4
    elif speed > 240:
        sensi = 0.3

    if speed >= 400:  # accelerate smoothly
        if frame_id - turn_frame < 500:
            actual_speed = 200
        else:
            actual_speed = min((frame_id - turn_frame - 500) * 0.5 + 100, speed)
        # sensi = max((speed - actual_speed) / 800 + 0.3, 0.3)
    else:
        actual_speed = speed

    db.drive(actual_speed, (l_co - r_co) * actual_speed * sensi)

    # Incrementing the frame_id
    frame_id += 1
