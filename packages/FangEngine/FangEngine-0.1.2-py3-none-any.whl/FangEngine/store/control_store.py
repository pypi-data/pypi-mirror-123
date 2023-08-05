"""
This module contains the ControlStore
"""
import typing
import os
import json
import pygame

UP = "up"
LEFT = "left"
JUMP = "jump"
DOWN = "down"
RIGHT = "right"
SPRINT = "backward"
CROUCH = "crouch"
FORWARD = "forward"
BACKWARD = "backward"

CONTROLS_FILE = os.path.join("assets", "settings", "controls.json")


class ControlStore:
    """
    The control store is a singleton which stores all control settings
    Default controls have been put in for convenience, however feel free to clear. I wont be offended.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ControlStore, cls).__new__(cls)

        return cls._instance

    def __init__(self, store: typing.Dict[str, int] = None):
        if store is None:
            store = {}

        self.store = {
            UP: pygame.K_w,
            LEFT: pygame.K_a,
            JUMP: pygame.K_SPACE,
            DOWN: pygame.K_s,
            RIGHT: pygame.K_d,
            SPRINT: pygame.K_LCTRL,
            CROUCH: pygame.K_LSHIFT,
            FORWARD: pygame.K_d,
            BACKWARD: pygame.K_a
        }

        self.store.update(store)

        try:
            with open(CONTROLS_FILE) as f:
                self.store.update(json.loads(f.read()))
        except FileNotFoundError:
            pass

    def __getitem__(self, item) -> int:
        return self.store[item]

    def __setitem__(self, key: str, value: int):
        self.store[key] = value

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return "<ControlStore controls={}>".format(len(self.store))

    def __iter__(self):
        for k, v in self.store.items():
            yield k, v

    def __delitem__(self, key):
        del self.store[key]

    def write_out(self):
        """
        Writes out the control settings to the control settings file
        This is recommended for whenever the player makes a change to the control settings
        :return:
        """
        try:
            with open(CONTROLS_FILE, 'w') as f:
                f.write(json.dumps(self.store, sort_keys=True))
        except FileNotFoundError:
            os.makedirs(os.path.join("assets", "settings"))

            with open(CONTROLS_FILE, 'w') as f:
                f.write(json.dumps(self.store, sort_keys=True))
