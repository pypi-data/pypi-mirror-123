"""
This module contains the image asset store
"""
import os

import pygame
import logging

import FangEngine.store.asset_store.asset_store as asset_store


class ImageAssetStore(asset_store.AssetStore):
    """
    By default, loads all assets saved in assets/images
    Images are saved with dot notation in all lowercase without the file extension

    For example, the image assets/images/player/player_top.png would be referenced by player.player_top

    Supported image formats:
    PNG, JPG, GIF, BMP
    """
    asset_path = os.path.join("assets", "images")

    def load_asset(self, path: str):
        try:
            return pygame.image.load(path)
        except pygame.error as e:
            logging.error("Failed to load asset '{}'. {}".format(path, e))
