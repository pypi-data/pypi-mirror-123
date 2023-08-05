"""
This module handles the conversion of angles from any unit of measure to radians (the units the engine uses)
"""
import math


def rotations(angle: float) -> float:
    """
    Converts number of rotations to radians
    """
    return angle * 2 * math.pi


def arc_minutes(angle: float) -> float:
    """
    Converts arc minutes to radians
    """
    return angle * (math.pi / 10800)


def arc_seconds(angle: float) -> float:
    """
    Converts arc seconds to radians
    """
    return angle * (math.pi / 648000)


def gradians(angle: float) -> float:
    """
    Converts gradians to radians
    """
    return angle * math.pi / 200


def degrees(angle: float) -> float:
    """
    Converts degrees to radians
    """
    return angle * math.pi / 180


def milliradians(angle: float) -> float:
    """
    Converts milliradians to radians
    """
    return angle / 1000


def radians(angle: float) -> float:
    """
    Converts radians to radians. This function was included for completeness.
    """
    return angle
