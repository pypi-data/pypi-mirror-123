import os

import pygame

import FangEngine.store.asset_store.asset_store as asset_store

pygame.mixer.init()


class SoundAssetStore(asset_store.AssetStore):
    """
    By default, loads all assets saved in assets/sounds
    Images are saved with dot notation in all lowercase without the file extension

    For example, the image assets/sounds/player/step.ogg would be referenced by player.step

    Supported formats (.ogg is preferred):
    OGG, MP3, XM, MOD
    """
    asset_path = os.path.join("assets", "sounds")

    def load_asset(self, path: str):
        return pygame.mixer.Sound(path)
