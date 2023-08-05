"""
This module contains the hitbox object
"""
import math
import typing
import pygame

if typing.TYPE_CHECKING:
    import FangEngine.game_object.game_object as game_object


class Hitbox:
    """
    Represents a rectangular hitbox of an object
    """
    def __init__(self, x: float, y: float, w: float, h: float):
        """
        :param x:
        :param y:
        :param w:
        :param h:
        """
        try:
            self.x = x
            self.y = y
            self.w = w
            self.h = h
        except AttributeError:
            # In this case, this is the BoundHitbox class and x, y, w and h are properties without setters
            pass

    def area(self) -> float:
        """
        Returns the area of the hitbox
        """
        return self.w * self.h

    def perimeter(self) -> float:
        """
        Returns the perimeter of the hitbox
        """
        return 2 * (self.w + self.h)

    def diagonal(self):
        """
        Returns the diagonal length of the hitbox
        """
        return math.sqrt(self.w ** 2 + self.h ** 2)

    def top_left(self) -> typing.Tuple[float, float]:
        """
        Returns the top left position of the hitbox
        """
        return self.x, self.y

    def bottom_left(self) -> typing.Tuple[float, float]:
        """
        Returns the bottom left position of the hitbox
        """
        return self.x, self.y + self.h

    def bottom_right(self) -> typing.Tuple[float, float]:
        """
        Returns the bottom right position of the hitbox
        """
        return self.x + self.w, self.y + self.h

    def top_right(self) -> typing.Tuple[float, float]:
        """
        Returns the to _right position of the hitbox
        """
        return self.x + self.w, self.y

    def is_point_colliding(self, x: float, y: float) -> bool:
        """
        Determines if the specified point is colliding with the hitbox
        """
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

    def is_hitbox_colliding(self, hitbox: 'Hitbox') -> bool:
        """
        Determines if the specified hitbox is colliding with the hitbox
        """
        if self.is_point_colliding(*hitbox.top_left()):
            return True

        elif self.is_point_colliding(*hitbox.bottom_left()):
            return True

        elif self.is_point_colliding(*hitbox.bottom_right()):
            return True

        elif self.is_point_colliding(*hitbox.top_right()):
            return True

        return False

    def draw_hitbox(self, buffer: pygame.Surface, color: typing.Tuple[int, int, int] = (255, 255, 255), width: int = 2):
        """
        Draws the hitbox to the specified buffer
        :param buffer:
        :param color:
        :param width: the line width to draw the hitbox (use 0 to fill)
        """
        pygame.draw.rect(buffer, color, (int(self.x), int(self.y), int(self.w), int(self.h)), width)

    def __repr__(self):
        return "<{} x={} y={} w={} h={}>".format(
            self.__class__.__name__, self.x, self.y, self.w, self.h
        )


class BoundHitbox(Hitbox):
    """
    A bound hitbox will follow and scale along with a derivative of the GameObject class
    """
    def __init__(self, child: 'game_object.GameObject'):
        """
        :param child: the object to bind the hitbox to
        """
        super().__init__(child.x, child.y, child.w, child.h)
        self.child = child

        self.x_offset = 0
        self.y_offset = 0
        self.w_offset = 0
        self.h_offset = 0

    @property
    def x(self):
        return self.child.x + self.x_offset

    @property
    def y(self):
        return self.child.y + self.y_offset

    @property
    def w(self):
        return self.child.w + self.w_offset

    @property
    def h(self):
        return self.child.h + self.h_offset
