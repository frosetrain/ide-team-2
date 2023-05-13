from .parameters import Stop
from .pupdevices import Motor

import colorlog
from logging import FileHandler

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter("%(log_color)s%(message)s"))
filehandle = FileHandler("first.log")

logger = colorlog.getLogger(__name__)
logger.setLevel("DEBUG")
logger.addHandler(handler)
logger.addHandler(filehandle)


class DriveBase:
    def __init__(
        self,
        left_motor: Motor,
        right_motor: Motor,
        wheel_diameter,
        axle_track,
    ):
        ...

    def drive(self, speed, turn_rate) -> None:
        logger.debug(f"db.drive({speed}, {turn_rate})")

    def stop(self) -> None:
        logger.debug("db.stop()")

    def settings(
        self,
        straight_speed=None,
        straight_acceleration=None,
        turn_rate=None,
        turn_acceleration=None,
    ) -> None:
        ...

    def straight(self, distance, then: Stop = Stop.HOLD, wait: bool = True) -> None:
        logger.debug(f"db.straight({distance})")

    def turn(self, angle, then: Stop = Stop.HOLD, wait: bool = True) -> None:
        logger.debug(f"db.turn({angle})")
