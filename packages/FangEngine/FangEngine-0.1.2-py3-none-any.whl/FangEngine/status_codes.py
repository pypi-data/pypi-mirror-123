"""
This module contains possible status codes for when the application terminates
"""
import enum


class StatusCodes(enum.Enum):
    """
    The status codes which could cause the application to stop
    """
    USER_QUIT = 0
