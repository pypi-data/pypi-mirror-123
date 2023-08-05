"""
This module contains rotatable text
"""
import typing

import pygame

import FangEngine.game_object.premade.rotatable_object as rotatable_object

pygame.font.init()


class RotatableText(rotatable_object.RotatableObject):
    """
    This class represents text with basic 3D rotational functionality
    This can only be used in a RotatableScreenBase screen or a derivative
    """
    def __init__(
            self, screen_parent, x: float, y: float, angle: float, distance: float, text: str,
            font: pygame.font.Font, color: typing.Tuple[int, int, int] = (255, 255, 255),
            background: typing.Tuple[int, int, int] = None, antialias: bool = True, bold: bool = False,
            italic: bool = False, underline: bool = False, *args, **kwargs
    ):
        """
        :param screen_parent:
        :param x: [unused]
        :param y:
        :param angle: The angle (in radians) to position the object at
        :param distance: The distance the object should be from the player
        :param text: The text the character can show. This can only have a length of 1
        :param font: The pygame font to render the character in
        :param color: the color of the character
        :param background: the background color of the character
        :param antialias: If the character should be rendered smooth (True) or not (False)
        :param bold: If the character should be bold
        :param italic: If the character should be italicized
        :param underline: If the character should be underlined
        :param args:
        :param kwargs:
        """
        self.font = font
        self.text = text
        self.color = color
        self.background = background
        self.antialias = antialias
        self.bold = bold
        self.italic = italic
        self.underline = underline

        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

        self.rendered_text = None       # type: pygame.Surface

        self.set_text(self.text)

        super().__init__(screen_parent, x, y, angle, distance, self.rendered_text, *args, **kwargs)

    def set_text(self, text: str):
        """
        Change the text which is displayed
        :param text:
        :return:
        """
        self.text = text
        self.rendered_text = self.font.render(self.text, True, self.color, self.background)
