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
    """Raise the sort, move backwards, then lower the sort."""
    # db.straight(-10)
    # about_turn()
    sort_motor.run_angle(250, 40)
    db.straight(-150)
    sort_motor.run_angle(250, 50)


def deposit(col) -> None:
    """Raise the sort, move backwards, then lower the sort."""
    db.straight(100)
    about_turn()
    db.straight(-50)
    sort_motor.run_angle(100, clock_angle(sort_motor.angle()-(colors[col]*90) + 30))
    db.straight(150)
    sort_motor.run_angle(100, 45)
    colors[col] = -1


def drive(x) -> None:
    """Do some line tracking."""
    l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
    r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
    # db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 275)
    db.drive(x, (l_co - r_co) * x * 0.80)
    # db.drive(x, 0)
    # 350, 250
    # Ratio of 7:5""


def about_turn() -> None:
    """Turn around 180 degrees."""
    db.turn(180)


turns = [
    0,   #0
    90,  #1
    -90, #2 
    45,  #3
    0,   #4
    0,   #5
    90,  #6
    0,   #7
    0,   #8
    45,  #9
    90,  #10
    0,   #11
    90,  #12
    45,  #13
    0,   #14
    0,   #15
    90,  #16
    0,   #17
    0,   #18
    45,  #19
    45,  #20
    0,   #21
    0,   #22
    90,  #23
    0,   #24
    0,   #25
    45,  #26
    90,  #27
    0,   #28
    90,  #29
    45,  #30
    0,   #31
    0,   #32
    90,  #33
    0,   #34
    0,   #35
    45,  #36

]

colors = {"red": -1, "yellow": -1, "green": -1, "blue": -1}
curr_angle = 0


def clock_angle(x):
    if x < 0:
        return 360 + x
    else:
        return x

        


if __name__ == "__main__":
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
            sort_motor.reset_angle(sort_motor.angle()%360)
        l_co = (l_sensor.reflection() - L_CO_BLACK) / L_CO_WHITE
        r_co = (r_sensor.reflection() - R_CO_BLACK) / R_CO_WHITE
        # print(l_co, r_co)

        if l_co > 0.6 and r_co < 0.05 and ons and straight > 2000:
            # We can merge this with the If below
            print("funny right turn!?!?!? ")
            db.straight(50, then=Stop.NONE)
            db.turn(turns[i])
            # db.turn(90)
            ons = False
            straight = 0
            i += 1

        if l_co + r_co < 0.08:

            if i == 4:
                db.straight(10, then=Stop.NONE)
            else:
                db.straight(50, then=Stop.NONE)

            if turns[i] != 0:
                print("turning...", i)
                db.stop()
                db.turn(turns[i])
                # db.turn(90)
            else:
                db.straight(15, then=Stop.NONE)
                print("unturn...", i)

            if i == 3 or i >= 5:
                # print("slow")
                speed = 140
                #db.settings(turn_rate=90)
            else:
                # print("speed")
                speed = 180

            if i == 9 or i == 26:
                print("start the straight")
                straight = 0
                ons = True

            if i == 21: #Deposit green
                deposit("green")
            if i == 24: #Deposit red
                deposit("red")
            if i == 31: #Deposit blue
                deposit("blue")
            if i == 34: #Deposit yellow
                deposit("yellow")


            i += 1
        # elif l_co > 0.7 and r_co > 0.7:
            # print("very white")
        drive(speed)
        if ons:
            straight += 1
            # print(straight)
                
        # l_ref = l_sensor.reflection()
        # r_ref = r_sensor.reflection()
        # l_hsv = l_sensor.hsv()
        # r_hsv = l_sensor.hsv()
        l_col = l_sensor.color()
        r_col = r_sensor.color()
        c_col = c_sensor.color()
        # print(l_ref, r_ref, l_col, l_hsv.h, l_hsv.s, l_hsv.v, r_col, r_hsv.h, r_hsv.s, r_hsv.v)
        # if l_col == Color.GREEN and r_col == Color.GREEN:  # green floor
        #     deposit()
        #     about_turn()
        #print(c_col)
        if c_col == Color.RED:
            db.stop()
            db.straight(-10)
            about_turn()
            pick_up()
            colors["red"] = curr_angle
            curr_angle += 1
        elif c_col == Color.YELLOW:
            db.stop()
            db.straight(-10)
            about_turn()
            pick_up()
            colors["yellow"] = curr_angle
            curr_angle += 1
        elif c_col == Color.GREEN:
            db.stop()
            db.straight(-10)
            about_turn()
            pick_up()
            colors["green"] = curr_angle
            curr_angle += 1
        elif c_col == Color.BLUE:
            db.stop()
            db.straight(-10)
            about_turn()
            pick_up()
            colors["blue"] = curr_angle
            curr_angle += 1
