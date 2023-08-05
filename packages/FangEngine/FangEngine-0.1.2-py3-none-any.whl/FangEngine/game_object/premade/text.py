"""
This module contains generic text which can be displayed
"""
import typing

import pygame

import FangEngine.game_object.game_object as game_object

pygame.font.init()


class Text(game_object.GameObject):
    """
    This class represents text which can be displayed on any derivative of the ObjectBase screen
    """
    def __init__(
            self, screen_parent, x: float, y: float, text: str,
            font: pygame.font.Font, color: typing.Tuple[int, int, int] = (255, 255, 255),
            background: typing.Tuple[int, int, int] = None, antialias: bool = True, bold: bool = False,
            italic: bool = False, underline: bool = False, *args, **kwargs
    ):
        """
        :param screen_parent:
        :param x:
        :param y:
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
        super().__init__(screen_parent, x, y, *args, **kwargs)

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

    def handle_input(self, keys: list, mouse: tuple, delta_t: float):
        pass

    def update(self, delta_t: float):
        pass

    def render(self, buffer: pygame.Surface):
        buffer.blit(self.rendered_text, self.convert_coords(self.x, self.y))

    def set_text(self, text: str):
        """
        Changes the text
        """
        self.text = text
        self.rendered_text = self.font.render(self.text, True, self.color, self.background)
        self.w, self.h = self.rendered_text.get_size()
