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
claw_motor = Motor(
    Port.A,
    positive_direction=Direction.CLOCKWISE,
    gears=None,
    reset_angle=True
)

l_sensor = ColorSensor(Port.E)
r_sensor = ColorSensor(Port.C)

db = DriveBase(left_motor, right_motor, 88, 128)


while True:
    #claw_motor.run_time(250, 500)
    #claw_motor.run_time(-250, 500)
    l_co = (l_sensor.reflection() - 5) / 50
    r_co = (r_sensor.reflection() - 6) / 53
    #db.drive((1 - abs(l_co - r_co)) * 350, (l_co - r_co) * 250)
    # db.drive(250, (l_co - r_co) * 300)
    # 350, 250 (7:5)
