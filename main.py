from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

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

l_sensor = ColorSensor(Port.E)
r_sensor = ColorSensor(Port.C)

db = DriveBase(left_motor, right_motor, 88, 128)
    
"""
    # l_co = (l_sensor.reflection() - 7)/55
    # r_co = (r_sensor.reflection() - 8)/58;
    # print(l_co, r_co)
    # wait(50)
    # MAX: 62, 66
    # MIN: 7, 8
"""

while True:
    l_co = (l_sensor.reflection() - 7) / 55
    r_co = (r_sensor.reflection() - 8) / 58
    #db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 275)
    db.drive(300, (l_co - r_co) * 475)
# 350, 250

#Ratio of 7:5
