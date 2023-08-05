"""
This module contains the base HUD (Heads Up Display) object
"""
import abc
import typing

import pygame
import time

import FangEngine.game_object.game_object as game_object
import FangEngine.store.asset_store.image_asset_store as image_asset_store

cs = image_asset_store.ImageAssetStore()

pygame.font.init()


class HUDBase(game_object.GameObject, abc.ABC):
    """
    This class is a parent class for all HUD (Heads Up Display) objects
    There is no requirement to use this base for a HUD
    """
    def __init__(
            self, screen_parent, x: float, y: float, w: float, h: float, font=pygame.font.Font,
            background_color: tuple = (255, 255, 255), left_padding: int = 5, middle_padding: int = 10
    ):
        """
        :param screen_parent: the screen which contains this object
        :param x: x draw position
        :param y: y draw position
        :param w: hud width
        :param h: hud height
        :param font: the Pygame font to render text in
        :param background_color: the background color of the HUD
        :param left_padding: the padding between the left of the screen and the first item
        :param middle_padding: the padding between different elements in the HUD
        """
        super().__init__(screen_parent, x, y)

        self.w = w
        self.h = h
        self.font = font
        self.background_color = background_color
        self.left_padding = left_padding
        self.middle_padding = middle_padding

        self.draw_y = self.y + ((self.h - self.font.get_height()) / 2)

        self.text = {}          # type: typing.Dict[str, pygame.Surface]

    def add_text(self, text: str, color=(0, 0, 0), ref_name: str = None):
        """
        This method adds text to the HUD
        :param text:
        :param color:
        :param ref_name: a name to uniquely reference this HUD element if you need to access/replace the text later
        If not specified you will not be able to access the text
        """
        if ref_name is None:
            ref_name = time.time_ns()

        self.text[ref_name] = self.font.render(text, True, color)

    def add_surface(self, surf: pygame.Surface, ref_name: str = None):
        """
        This method adds any Pygame surface to the HUD
        The surface will be scaled down to be as tall as the HUD
        :param surf:
        :param ref_name: a name to uniquely reference this HUD element if you need to access/replace the text later
        If not specified you will not be able to access the text
        """
        if ref_name is None:
            ref_name = time.time_ns()

        surf = pygame.transform.scale(surf, (int(surf.get_width() * (self.font.get_height() / surf.get_height() )), self.font.get_height()))
        self.text[ref_name] = surf

    def add_image(self, name: str, ref_name: str = None):
        """
        This method adds any image from the image store to the HUD
        The image will be scaled down to be as tall as the HUD
        :param name:
        :param ref_name: a name to uniquely reference this HUD element if you need to access/replace the text later
        If not specified you will not be able to access the text
        """

        if ref_name is None:
            ref_name = time.time_ns()

        self.add_surface(cs.get(name), ref_name=ref_name)

    def render(self, buffer: pygame.Surface):
        """
        Draws the HUD and all contained elements to the specified buffer
        """
        super(HUDBase, self).render(buffer)
        pygame.draw.rect(buffer, self.background_color, (self.x, self.y, self.w, self.h))

        x = self.left_padding
        for text in self.text.values():
            buffer.blit(text, (x, self.draw_y))
            x += text.get_width() + self.middle_padding

    def on_click(self, pos: tuple, button: int):
        """
        Run this method to simulate a click on the HUD
        Override this method to change the click event
        If a HUD item is clicked, the on_hud_item_click event will be triggered
        """
        cx, cy = pos

        x = self.left_padding
        for name, surf in self.text.items():
            if x <= cx <= x + surf.get_width() and self.draw_y <= cy <= self.draw_y + surf.get_height():
                self.on_hud_item_click(str(name))

            x += surf.get_width() + self.middle_padding

    def on_hud_item_click(self, ref_name: str):
        """
        This event is triggered when a HUD item is clicked
        Note that even non-named items will trigger this event. Their name will be a float.
        :param ref_name: the name of the HUD item (set when added)
        """
        pass

    def remove_item(self, ref_name: str) -> pygame.Surface:
        """
        Removes the specified item from the HUD
        :param ref_name: the name of the HUD item (set when added)
        """
        return self.text.pop(ref_name)
