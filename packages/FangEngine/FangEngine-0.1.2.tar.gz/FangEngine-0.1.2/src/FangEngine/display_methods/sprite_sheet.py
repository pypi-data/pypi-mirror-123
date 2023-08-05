"""
This module contains the sprite sheet class for animated images
"""
import time
import typing

import pygame

import FangEngine.store as store

image_store = store.ImageAssetStore()
sound_store = store.SoundAssetStore()


class SpriteSheet:
    """
    This class represents a single sprite sheet
    Animation moves from left to right and top to bottom
    """
    def __init__(
            self, image: str, tiles_wide: int, tiles_high: int, frames: int, speed: float = 0.1,
            scale_w: float = 1, scale_h: float = 1, color_key: typing.Tuple[int, int, int] = (255, 0, 255)
    ):
        """
        :param image: the name of the image to retrieve from the image store
        :param tiles_wide: the number of tiles wide in the animation
        :param tiles_high: the number of tiles high in the animation
        :param frames: the total number of frames in the animation
        For example, in a 3x3 animation, if there are only 7 frames, then set this number to 7
        :param speed: the number of seconds to remain on each frame
        :param scale_w: the factor to scale the image horizontally
        :param scale_h: the factor to scale the image vertically.
        While the default is 1, if None is provided, this will be set to scale_w
        :param color_key: an RGB color to be used as the invisible color (any color not included in any of the frames)
        """
        if scale_h is None:
            scale_h = scale_w

        self.image_name = image
        self.image = image_store.get(image)            # type: pygame.Surface

        self.tiles_wide = tiles_wide
        self.tiles_high = tiles_high
        self.speed = speed
        self.scale_w = scale_w
        self.scale_h = scale_h
        self.frame_count = frames
        self.color_key = color_key

        self.frame = 0
        self.next_change = 0

        self.image = pygame.transform.scale(
            self.image, (
                int(self.image.get_width() * self.scale_w), int(self.image.get_height() * self.scale_h)
            )
        )

        self.tile_w = self.image.get_width() / self.tiles_wide
        self.tile_h = self.image.get_height() / self.tiles_high

    def render(self, buffer: pygame.Surface, x: float, y: float):
        """
        Draws the sprite sheet to the specified buffer at the specified location
        """
        buffer.blit(self.image, (x, y))

    def get_current_image(self) -> pygame.Surface:
        """
        Returns the current frame the animation is on
        """
        if time.time() >= self.next_change:
            self.next_change = time.time() + self.speed
            self.frame += 1
            if self.frame >= self.frame_count:
                self.frame = 0

        x = self.frame % self.tiles_wide
        y = self.frame // self.tiles_wide

        return self.image_at(x * self.tile_w, y * self.tile_h, self.tile_w, self.tile_h)

    def image_at(self, x: float, y: float, w: float, h: float, color_key=None) -> pygame.Surface:
        """
        Returns a subsection of the image
        if color_key is not set, the color key of the spritesheet will be used instead
        """
        if color_key is None:
            color_key = self.color_key

        rect = pygame.Rect((x, y, w, h))
        image = pygame.Surface(rect.size).convert()
        image.fill(color_key)
        image.blit(self.image, (0, 0), rect)
        image.set_colorkey(color_key, pygame.RLEACCEL)

        return image
