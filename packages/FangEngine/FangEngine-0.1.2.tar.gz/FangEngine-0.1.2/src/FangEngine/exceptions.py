"""
This module stores custom exceptions the engine may raise
"""


class UnknownColorException(ValueError):
    """
    This exception is raised when the user attempts to get a color by name that is not in the enum
    """
