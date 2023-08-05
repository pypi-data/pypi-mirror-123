"""
This module contains the camera class
"""
import typing


class Camera:
    """
    This is the camera object for moving around a scene
    """
    def __init__(self, x: float = 0, y: float = 0):
        """
        :param x:
        :param y:
        """
        self.x = x
        self.y = y
        self.move_callbacks = []        # type: typing.List[callable]

    def get_pos(self) -> typing.Tuple[float, float]:
        """
        Returns the coordinates of the camera
        """
        return self.x, self.y

    def move(self, x: float = 0, y: float = 0):
        self.x += x
        self.y += y

        self.on_move(x, y)

    def on_move(self, dx, dy):
        for c in self.move_callbacks:
            c(-dx, -dy)
