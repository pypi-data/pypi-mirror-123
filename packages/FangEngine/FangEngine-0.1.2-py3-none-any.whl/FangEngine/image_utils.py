"""
This module contains utilities for image processing
"""
import pygame


def scale_image(image: pygame.Surface, factor: float):
    """
    Scales the specified image by the specified scale factor
    """
    size = image.get_size()
    return pygame.transform.scale(image, (int(size[0] * factor), int(size[1] * factor)))
