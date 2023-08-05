"""
This module contains the base game object
"""
import abc
import typing

import pygame

import FangEngine.game_object.hitbox as hitbox
import FangEngine.store.asset_store.image_asset_store as image_asset_store
import FangEngine.store.asset_store.sound_asset_store as sound_asset_store

if typing.TYPE_CHECKING:
    import FangEngine.screen_manager.dialog_box as dialog_box
    import FangEngine.screen_manager.base_screen as base_screen
    import FangEngine.screen_manager.camera as camera


class GameObject(abc.ABC):
    """
    This is the base class for any object that can be displayed on any derivative of the ObjectBase screen
    """
    IMAGE_STORE = image_asset_store.ImageAssetStore()
    SOUND_STORE = sound_asset_store.SoundAssetStore()

    def __init__(self, screen_parent: 'base_screen.BaseScreen', x: float, y: float, *args, **kwargs):
        """
        :param screen_parent:
        :param x:
        :param y:
        :param args:
        :param kwargs:
        """
        self.screen_parent = screen_parent

        self.x = x
        self.y = y
        self.last_x = x
        self.last_y = y

        self.w = 0
        self.h = 0

        self.hitbox = hitbox.BoundHitbox(self)

        self.visible = True

    def show(self):
        self.visible = True
        self.on_visibility_change(self.visible)

    def hide(self):
        self.visible = False
        self.on_visibility_change(self.visible)

    def set_visibility(self, visible: bool):
        self.visible = visible
        self.on_visibility_change(self.visible)

    def on_visibility_change(self, state: bool):
        pass

    def on_message_receive(self, message: typing.Union[list, tuple, str], sender):
        """
        This event is run when another object on the same screen broadcasts a message
        :param message:
        :param sender: the sender of the message
        """
        pass

    def broadcast_message(self, message: typing.Union[list, tuple, str]):
        """
        Broadcasts a message to all other objects on this screen
        :param message: the message to send
        """
        self.screen_parent.broadcast_message(message, self)

    def class_name(self) -> str:
        """
        Returns the name of the class
        """
        return self.__class__.__name__

    @property
    def camera(self) -> 'camera.Camera':
        """
        Returns the camera object on this screen
        """
        return self.screen_parent.camera

    @property
    def screen_w(self) -> int:
        """
        Returns the width of the screen
        :return:
        """
        return self.screen_parent.screen_manager.screen_w

    @property
    def screen_h(self) -> int:
        """
        Returns the height of the screen
        :return:
        """
        return self.screen_parent.screen_manager.screen_h

    def convert_coords(self, x: float, y: float) -> typing.Tuple[float, float]:
        """
        Scales coordinates with respect to the the scaling of the screen
        This is especially useful for interacting with the mouse directly
        """
        return self.screen_parent.convert_coords(x, y)

    def on_create(self, *args, **kwargs):
        """
        This event is triggered when this object is created
        It is run once and only once
        """
        pass

    def show_dialog_box(self, box: 'dialog_box.DialogBox.__class__', *args, **kwargs):
        """
        This method causes the screen to show a dialog box
        :param box: the class reference to the dialog box
        :param args:
        :param kwargs:
        """
        self.screen_parent.show_dialog_box(box, *args, **kwargs)

    @abc.abstractmethod
    def handle_input(self, keys: list, mouse: tuple, delta_t: float):
        """
        This event allows the handling of user input
        This event is triggered every frame
        :param keys: A list of keys and their states. The index of a key is its ASCII value (use pygame constants)
        :param mouse: the state of the mouse buttons
        :param delta_t: the amount of time (in seconds) that has passed since the last frame
        """

    @abc.abstractmethod
    def update(self, delta_t: float):
        """
        This event is triggered every frame. This is where the main update code should go
        :param delta_t: the amount of time (in seconds) that has passed since the last frame
        """
        if self.last_x != self.x or self.last_y != self.y:
            self.on_move(self.x - self.last_x, self.y - self.last_y)

            self.last_x = self.x
            self.last_y = self.y

            self.check_collision()

    def move(self, dx: float, dy: float):
        """
        This moves the object by a factor of dx/dy and triggers the on_move event
        """
        self.x += dx
        self.y += dy
        self.on_move(dx, dy)

    def check_collision(self):
        """
        Causes this object to check for collisions with other objects
        If a collision is detected, the on_collide event of both objects will be triggered
        """
        self.screen_parent.check_collisions(self)

    @abc.abstractmethod
    def render(self, buffer: pygame.Surface):
        """
        This event is triggered every frame
        THis event should be used for drawing the object to the buffer ONLY
        Use the update event for other updates
        :param buffer: the buffer to draw to
        """
        pass

    def on_key_down(self, unicode, key, mod):
        pass

    def on_key_up(self, key, mod):
        pass

    def on_mouse_motion(self, pos, rel, buttons):
        pass

    def on_mouse_button_up(self, pos, button):
        pass

    def on_mouse_button_down(self, pos, button):
        pass

    def on_joystick_axis_motion(self, joystick, axis, value):
        pass

    def on_joystick_ball_motion(self, joystick, ball, rel):
        pass

    def on_joystick_hat_motion(self, joystick, hat, value):
        pass

    def on_joystick_button_up(self, joystick, button):
        pass

    def on_joystick_button_down(self, joystick, button):
        pass

    def on_screen_enter(self, previous_screen: str):
        pass

    def on_screen_leave(self, next_screen: str):
        pass

    def on_move(self, dx: float, dy: float):
        pass

    def on_collide(self, other: 'GameObject'):
        pass

    def on_click(self, pos: tuple, button: int):
        pass
