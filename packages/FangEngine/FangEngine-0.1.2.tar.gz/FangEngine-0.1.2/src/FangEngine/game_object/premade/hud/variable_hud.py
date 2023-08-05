"""
This module contains the VariableHUD class (WIP)
"""
import typing

import pygame
import collections
import abc

import FangEngine.game_object.premade.hud.hud_base as hud_base


class VariableHUD(hud_base.HUDBase):
    """
    This class represents the VariableHUD class (WIP)
    It will keep its values up to date based on return values of other methods

    This class is a work in progress and is not ready for use yet
    """
    def __init__(self, screen_parent, x: float, y: float, w: float, h: float):
        raise NotImplementedError("Coming Soon")

        super().__init__(screen_parent, x, y, w, h)
        self.metrics = collections.OrderedDict()        # type: typing.Dict[str, callable]

    def add_metric(self, name: str, function: callable) -> 'VariableHUD':
        self.metrics[name] = function
        return self
