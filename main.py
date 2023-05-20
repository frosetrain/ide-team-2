"""This is the code for IDE Team 2!!!!"""

from pybricks.hubs import PrimeHub
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.pupdevices import ColorSensor, Motor
from pybricks.robotics import DriveBase
from pybricks.tools import StopWatch, wait

watch = StopWatch()

L_CO_BLACK = 12
R_CO_BLACK = 12
L_CO_WHITE = 92
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
    Turn(0), #2
    #collect first ferti
    Turn(0), #3
    Turn(0), #4
    Turn(0), #5
    Turn(0), #6
    #collect second ferti
    # At this moment, we know exactly where on the West side we need to go
]

# Storing where each cube is in the sorter
sort_slots = {
    0: "",
    1: "",
    2: "",
    3: "",
}

fert_is_red = False
fert_is_green = False
fert_is_yellow = False
fert_is_blue = False
slot_order = []
isPicked = False
toCharge = False
current_slot = 0  # The currently open sort-slot
turn_number = 0  # This variable was previously called i
turn_frame = 0  # The frame where the robot last turned
on_straight = False  # Whether we are on a straight
colored_floor_count = (
    0  # Counting how long we are on a colored area without encountering a cube
)
speed = 240  # The speed of the robot
frame_id = 0  # How many times the while loop has run

# sort_motor.reset_angle()
sort_motor.run_target(100, -15)
print(sort_motor.angle())



def charge():
    db.straight(200)
    db.turn(180)
    wait(2500)
    db.straight(160)

while True:
    l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    l_col = l_sensor.color()
    r_col = r_sensor.color()
    c_col = c_sensor.color()

    if sort_motor.angle() < 0 or sort_motor.angle() > 359:
        sort_motor.reset_angle(sort_motor.angle() % 360)

    goofy = (l_co > 0.6 and r_co < 0.08) or (l_co < 0.08 and r_co > 0.6)
    funny_turn = goofy and on_straight and frame_id - turn_frame > 1000
    if funny_turn:
        print("funny turn!?!?!? ")
        on_straight = False
        straight_count = 0

    # Detecting turns (including funny ones)
    if l_co + r_co < 0.1 or funny_turn:
        # print(l_co, r_co)
        turn = TURNS[turn_number]
        # hub.display.number(turn_number)
        turn_frame = frame_id
        # print(turn_frame)

        if turn.angle != 0:  # A real turn
            # db.stop()
            # db.curve(50, turn.angle, then=Stop.COAST)

            db.straight(36, then=Stop.NONE)
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
        
        turn_number += 1
        
    # Pick up
    color = str(c_col)[6:]

    if turn_number == 3 or turn_number == 6:
        print("PICKING")
        
        db.straight(20)
        color = str(c_sensor.color())[6:]
        db.turn(180, wait=False)
        sort_motor.run_angle(200, 40)
        while not db.done():
            pass
        db.straight(-155)
        sort_motor.run_angle(200, 50)
        print(color)
        print(current_slot)
        sort_slots[current_slot] = color
        if turn_number < 5:
            db.straight(170)
        else:
            db.straight(40)
            print("LMAOOOOOOOOOOOOOOO")
            cubes = 2
            for item in sort_slots:
                if sort_slots[item] == "GREEN":
                    fert_is_green = True
                    print("There is GREEN")
                elif sort_slots[item] == "RED":
                    fert_is_red = True
                    print("There is RED")
                elif sort_slots[item] == "BLUE":
                    fert_is_blue = True
                    print("There is BLUE")
                elif sort_slots[item] == "YELLOW":
                    fert_is_yellow = True
                    print("There is YELLOW")

            if fert_is_green:
                if sort_slots[0] == "GREEN":
                    slot_order.append(0)
                else:
                    slot_order.append(1)
                TURNS.extend([Turn(90, 499), Turn(45, 140), Turn(0)])
                cubes -= 1
                fert_is_green = False
                
                if fert_is_red:
                    if sort_slots[0] == "RED":
                        slot_order.append(0)
                    else:
                        slot_order.append(1)
                    TURNS.extend([Turn(90), Turn(0)])
                    cubes -= 1
                    TURNS.extend([Turn(45, 500, True)])
                    fert_is_red = False

                    
                else:
                    TURNS.extend([Turn(-45, 500, True)])

            if fert_is_red:
                if sort_slots[0] == "RED":
                    slot_order.append(0)
                else:
                    slot_order.append(1)
                TURNS.extend([Turn(90, 499), Turn(-45, 140), Turn(0)])
                fert_is_red = False
                    
                TURNS.extend([Turn(90, 499)])
            

            if toCharge:
                TURNS.extend([Turn(-90, 240)])
            else:
                TURNS.extend([Turn(0, 499)])
                TURNS.extend([Turn(90)])
                if fert_is_blue:
                    if sort_slots[0] == "BLUE":
                        slot_order.append(0)
                    else:
                        slot_order.append(1)
                    TURNS.extend([Turn(90, 499), Turn(45, 140), Turn(0)])
                    cubes -= 1
                    fert_is_blue = False
                
                if cubes == 0:

                    TURNS.extend([Turn(-45, 500, True), Turn(-90, 499), Turn(90, 240)])
                else:
                    if sort_slots[0] == "GREEN":
                        slot_order.append(0)
                    else:
                        slot_order.append(1)
                    TURNS.extend([Turn(90, 499), Turn(0)])
                    fert_is_yellow = False
                    TURNS.extend([Turn(45, 500, True), Turn(-90, 499), Turn(90, 240)])
                    
            
            isPicked = True

        turn_number += 1
        
        current_slot += 1

    if color == "BLACK" and turn_number > 8:
        print("DEPOSITING NOW!!!")
        db.straight(120)
        db.turn(178)
        slot = -1
        for item in sort_slots:
            if sort_slots[item] == sort_slots[0]:
                slot = item
                print(sort_slots[0], "is in ", slot)
                break
        angle_difference = (
            slot * 90 - sort_motor.angle() + 12
        )
        if angle_difference < 0:
            angle_difference += 360
            print(angle_difference)
        db.straight(-20)
        sort_motor.run_angle(200, angle_difference)
        db.straight(75)
        sort_motor.run_angle(200, 40)
        sort_slots[slot] = -1
        current_slot = slot
        slot_order = slot_order[1:]
        print("PICKING")
        sort_motor.run_angle(200, 40)
        while not db.done():
            pass
        db.straight(-160)
        sort_motor.run_angle(200, 50)
        print(color)
        print(current_slot)
        sort_slots[current_slot] = color
        db.straight(150)
        current_slot += 1
    if turn_number == len(TURNS) and turn_number > 9:
        toCharge = True
    
    if turn_number == len(TURNS) and toCharge:
        print("i charge")
        charge()
        toCharge = False
        TURNS.extend([
    Turn(0), 
    Turn(-90), 
    Turn(-90, 499),
    Turn(45, 145),
    Turn(0),
    Turn(90),
    Turn(0),
    Turn(45, 500, True),
    Turn(90, 499),
    Turn(0),
    Turn(90),
    Turn(45, 145),
    Turn(0),
    Turn(90),
    Turn(0),
    ])



    if turn_number == 6 and isPicked == False:
        continue
                
    # Line tracking
    if speed < 240:
        sensi = 0.69
    elif speed == 240:
        sensi = 0.4
    elif speed > 240:
        sensi = 0.3
    
    if speed >= 500:  # accelerate smoothly
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
    
