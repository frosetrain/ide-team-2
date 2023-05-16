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
turns: list[Turn] = [
    Turn(0, 240),  # 0, starting with normal speed
    Turn(90),  # 1
]

TURNS_RED: list[Turn] = [
    Turn(-90, 300),  # 2
    Turn(-45, 150),  # 3
    Turn(0),  # 4
    Turn(0),  # 5
]

TURNS_YELLOW: list[Turn] = [
    Turn(90, 300),  # 2
    Turn(-45, 150),  # 3
    Turn(0),  # 4
    Turn(0),  # 5
]

# List of turns where cubes can be deposited
DEPOSITS = {4: "RED", 4: "BLUE"}

# Storing where each cube is in the sorter
sort_slots = {
    "RED": 1,
    "YELLOW": 3,
    "GREEN": 2,
    "BLUE": 0,
}
current_slot = 0  # The currently open sort-slot
turn_number = 0  # This variable was previously called i
turn_frame = 0  # The frame where the robot last turned
on_straight = False  # Whether we are on a straight
colored_floor_count = (
    0  # Counting how long we are on a colored area without encountering a cube
)
speed = 240  # The speed of the robot
frame_id = 0  # How many times the while loop has run
branch = ""

# sort_motor.reset_angle()
sort_motor.run_target(100, -15)
print(sort_motor.angle())

while True:
    l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    l_col = l_sensor.color()
    r_col = r_sensor.color()
    c_col = c_sensor.color()

    the = [Color.RED, Color.YELLOW]
    if l_col in the and r_col in the and turn_number > 2:
        break
    
    # print(l_co, r_co, l_col, r_col, c_col)

    if sort_motor.angle() < 0 or sort_motor.angle() > 359:
        sort_motor.reset_angle(sort_motor.angle() % 360)

    funny_turn = l_co > 0.6 and r_co < 0.08 and on_straight and frame_id - turn_frame > 1000
    if funny_turn:
        print("funny right turn!?!?!? ")
        on_straight = False
        straight_count = 0

    # Detecting turns (including funny ones)
    if l_co + r_co < 0.2 or funny_turn:
        print(turn_number)
        if turn_number == 2:
            while c_col not in [Color.RED, Color.YELLOW]:
                db.drive(240, 0)
                c_col = c_sensor.color()
            db.stop()
            if c_col == Color.RED:
                print("RED")
                turns.extend(TURNS_RED)
            if c_col == Color.YELLOW:
                print("YELLOW")
                turns.extend(TURNS_YELLOW)
            db.straight(-30)

        turn = turns[turn_number]
        # hub.display.number(turn_number)
        turn_frame = frame_id
        print(turn_frame)

        if turn.angle != 0:  # A real turn
            # db.stop()
            # db.curve(50, turn.angle, then=Stop.COAST)

            db.straight(50, then=Stop.NONE)
            print("turning... " + str(turn_number))
            db.stop()
            db.turn(turn.angle)
        else:  # Continue straight
            db.straight(25, then=Stop.NONE)
            print("unturn... " + str(turn_number))

        if turn.speed is not None:  # If a new speed is specified
            speed = turn.speed
            db.settings(straight_speed=speed)
            print(f"new speed {speed}")

        if turn.begin_straight:
            print("start the straight")
            on_straight = True
        else:
            on_straight = False

        if turn_number in DEPOSITS.keys():  # If a cube should be deposited here
            db.straight(100)
            db.turn(180)
            angle_difference = (
                sort_slots[DEPOSITS[turn_number]] * 90 - sort_motor.angle() + 10
            )
            if angle_difference < 0:
                angle_difference += 360
            sort_motor.run_angle(250, angle_difference)
            db.straight(75)
            sort_motor.run_angle(250, 40)
            sort_slots[DEPOSITS[turn_number]] = -1

        turn_number += 1
        continue  # we go back to the top of while True to get new sensor values

    # Handling cases where there are no cubes on a colored floor
    if (
        l_col != Color.NONE
        and l_col != Color.WHITE
        and r_col != Color.NONE
        and r_col != Color.WHITE
        and False
    ):
        colored_floor_count += 1
    else:
        colored_floor_count = 0

    if colored_floor_count >= 80 and turn_number > 1:
        colored_floor_count = 0
        db.turn(180)
        db.straight(50)
        turn_number += 0

    # Picking up cubes if we see any
    # TODO: Only pick up cubes if it's in a valid position
    color = str(c_col)[6:]
    #color = c_col
    if color in ["RED", "YELLOW", "GREEN", "BLUE"]:
        # db.stop()
        # db.straight(-10)
        db.turn(180, wait=False)
        # print("Pick up")
        sort_motor.run_angle(250, 40)
        while not db.done():
            pass
        db.straight(-155)
        sort_motor.run_angle(250, 50)
        sort_slots[color] = current_slot
        current_slot += 1
        continue

    # Line tracking
    if speed < 240:
        sensi = 0.69
    elif speed == 240:
        sensi = 0.5
    elif speed > 240:
        sensi = 0.4
    
    if speed >= 300:  # accelerate smoothly
        if frame_id - turn_frame < 500:
            actual_speed = 100
        else:
            actual_speed = min((frame_id - turn_frame - 500) * 0.5 + 100, speed)
        # sensi = max((speed - actual_speed) / 800 + 0.3, 0.3)
    else:
        actual_speed = speed

    db.drive(actual_speed, (l_co - r_co) * actual_speed * sensi)
    
    # Incrementing the frame_id
    frame_id += 1
