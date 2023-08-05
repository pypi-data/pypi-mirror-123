"""
This module contains the clickable text object
"""
import typing

import pygame

import FangEngine.game_object.game_object as game_object

pygame.font.init()


class CharacterButton(game_object.GameObject):
    """
    This class represents text which can be clicked on
    This can be displayed on any derivative of the ObjectBase screen
    """
    def __init__(
            self, screen_parent, x: float, y: float, text: str,
            font: pygame.font.Font, color: typing.Tuple[int, int, int] = (255, 255, 255),
            background: typing.Tuple[int, int, int] = None, antialias: bool = True, bold: bool = False,
            italic: bool = False, underline: bool = False, outline_color: typing.Tuple[int, int, int] = None,
            outline_radius: int = 5, outline_width: int = 3, click_event: callable = None, *args, **kwargs
    ):
        """
        :param screen_parent:
        :param x:
        :param y:
        :param text: the text on the button
        :param font: the pygame font to render the text in
        :param color: the text color
        :param background: the background color of the button
        :param antialias:
        :param bold:
        :param italic:
        :param underline:
        :param outline_color:
        :param outline_radius:
        :param outline_width:
        :param click_event: the reference to the function to run when clicked.
        The function must take 2 parameters.
        Alternatively you can make a child class and override the on_click method
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
        self.outline_color = outline_color
        self.outline_radius = outline_radius
        self.outline_width = outline_width

        if click_event is not None:
            self.on_click = click_event

        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

        self.rendered_text = self.font.render(self.text, True, self.color, self.background)
        if self.outline_color is not None:
            size = max(self.rendered_text.get_size()) + 10
            surf = pygame.Surface((size, size))
            surf.fill((0, 0, 0) if self.background is None else self.background)
            surf.blit(self.rendered_text, (
                (size / 2) - (self.rendered_text.get_width() / 2), (size / 2) - (self.rendered_text.get_height() / 2)
            ))
            self.rendered_text = surf

            pygame.draw.rect(
                self.rendered_text, self.outline_color, (0, 0, size, size),
                self.outline_width, self.outline_radius
            )

            self.w, self.h = self.rendered_text.get_size()

    def handle_input(self, keys: list, mouse: tuple, delta_t: float):
        pass

    def update(self, delta_t: float):
        pass

    def render(self, buffer: pygame.Surface):
        """
        Draws the button to the buffer
        """
        buffer.blit(self.rendered_text, self.convert_coords(self.x, self.y))
