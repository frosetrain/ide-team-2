"""This is the code for IDE Team 2!!!!"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

L_CO_BLACK = 8
R_CO_BLACK = 7
L_CO_WHITE = 66
R_CO_WHITE = 61

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
    #0, 
    90,  # 22
    0,  # 23
    #0, 
    45,  # 24
    90,  # 25
    0,  #26
    90,  # 27
    45,  # 28
    0,  # 29
    #0,  
    90,  # 30
    0,  # 31
    #0, 
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
db.settings(straight_speed=180)


def pick_up() -> None:
    """Pick up a cube from a colored area."""
    sort_motor.run_angle(250, 40)
    db.straight(-150)
    sort_motor.run_angle(250, 50)


def deposit(col) -> None:
    """Raise the sort, move backwards, then lower the sort."""
    db.straight(100)
    about_turn()
    # db.straight(-50)
    print()
    sort_motor.run_angle(100, clock_angle((colors[col] * 90 + 10) - (sort_motor.angle())))
    db.straight(75)
    sort_motor.run_angle(100, 45)
    colors[col] = -1


def drive(x) -> None:
    """Do some line tracking."""
    l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    # db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 275)
    db.drive(x, (l_co - r_co) * x * 0.85)


def about_turn() -> None:
    """Turn around 180 degrees."""
    db.turn(180)


def clock_angle(x):
    if x < 0:
        print(360 + x)
        return 360 + x
    else:
        print(x)
        return x


if __name__ == "__main__":
    colors = {"RED": 1, "YELLOW": 3, "GREEN": 2, "BLUE": 0}
    curr_angle = 0
    i = 0
    speed = 180
    straight = 0
    turned = 0
    ons = False
    sort_motor.run_target(100, -15)

    while False:
        # l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
        # r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
        print(l_sensor.reflection(), r_sensor.reflection())
    while True:
        if sort_motor.angle() < 0 or sort_motor.angle() > 359:
            sort_motor.reset_angle(sort_motor.angle() % 360)
        l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
        r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
        # print(l_co, r_co)
        # print(ons, straight)
        if l_co > 0.58 and r_co < 0.05 and ons and straight > 500:
            # We can merge this with the If below
            print("funny right turn!?!?!? ")
            db.straight(50, then=Stop.NONE)
            db.turn(TURNS[i])
            # db.turn(90)
            ons = False
            straight = 0
            i += 1

        if l_co + r_co < 0.1:
            if i == 4:
                db.straight(10, then=Stop.NONE)
            else:
                db.straight(50, then=Stop.NONE)

            if TURNS[i] != 0:
                print("turning...", i)
                db.stop()
                db.turn(TURNS[i])
                # db.turn(90)
            else:
                db.straight(15, then=Stop.NONE)
                print("unturn...", i)

            if i == 3 or i >= 5:
                # print("slow")
                speed = 140
            else:
                # print("speed")
                speed = 180

            if i == 9 or i == 24:
                print("start the straight")
                straight = 0
                ons = True

            if i == 21:
                deposit("GREEN")
            if i == 23:
                deposit("RED")
            if i == 29:
                deposit("BLUE")
            if i == 31:
                deposit("YELLOW")
            i += 1
        
        drive(speed)

        if ons:
            straight += 1
            # print(straight)

        l_col = l_sensor.color()
        r_col = r_sensor.color()
        c_col = c_sensor.color()

        color = str(c_col)[6:]
        #print(color)
        if color in ["RED", "YELLOW", 'GREEN', 'BLUE']:
            db.stop()
            db.straight(-10)
            about_turn()
            pick_up()
            colors[color] = curr_angle
            curr_angle += 1
