"""
This module contains the BaseScreen. The parent class of all screens
"""
import abc
import typing

import pygame

import FangEngine.screen_manager.camera as camera

if typing.TYPE_CHECKING:
    import FangEngine.screen_manager.dialog_box as dialog_box
    import FangEngine.screen_manager.screen_manager as screen_manager


class BaseScreen(abc.ABC):
    """
    The BaseScreen is the object all screens MUST inherit from
    """
    def __init__(self, name: str, manager, *args, **kwargs):
        self.name = name                        # type: str
        self.screen_manager = manager           # type: screen_manager.ScreenManager
        self.dialog_boxes = []                  # type: typing.List[dialog_box.DialogBox]
        self.PIXELS_PER_METER = 100
        self.fill_background_color = (0, 0, 0)       # type: typing.Union[None, typing.Tuple[int, int, int]]
        self.camera = camera.Camera()

    def on_create(self):
        """
        This event is triggered when the screen is created
        It is run once and only once
        """
        pass

    @property
    def screen_w(self) -> int:
        """
        Returns the width of the screen
        """
        return self.screen_manager.screen_w

    @property
    def screen_h(self) -> int:
        """
        Returns the height of the screen
        """
        return self.screen_manager.screen_h

    def center_mouse(self):
        """
        Moves the mouse cursor to the center of the screen
        """
        pygame.mouse.set_pos(
            int(self.screen_w / 2), int(self.screen_h / 2)
        )
        pygame.event.clear(pygame.MOUSEMOTION, pump=False)
        pygame.mouse.get_rel()

    def center_mouse_x(self):
        """
        Moves the mouse cursor so it is centered along the x axis
        """
        curr = pygame.mouse.get_pos()
        pygame.mouse.set_pos(
            int(self.screen_w / 2), curr[1]
        )
        pygame.event.clear(pygame.MOUSEMOTION, pump=False)
        pygame.mouse.get_rel()

    def center_mouse_y(self):
        """
        Moves the mouse cursor so it is centered along the y axis
        """
        curr = pygame.mouse.get_pos()
        pygame.mouse.set_pos(
            curr[0], int(self.screen_h / 2)
        )
        pygame.event.clear(pygame.MOUSEMOTION, pump=False)
        pygame.mouse.get_rel()

    def hide_mouse(self):
        """
        Hides the mouse cursor
        """
        pygame.mouse.set_visible(False)

    def show_mouse(self):
        """
        Shows the mouse cursor
        """
        pygame.mouse.set_visible(True)

    def is_showing_dialog_box(self) -> bool:
        """
        Returns if there are any dialog boxes currently being displayed
        """
        return len(self.dialog_boxes) > 0

    def show_dialog_box(self, box: 'dialog_box.DialogBox.__class__', *args, **kwargs):
        """
        Shows a new dialog box
        :param box: the reference to the dialog box class to show
        :param args:
        :param kwargs:
        """
        self.dialog_boxes.insert(0, box(self, *args, **kwargs))

    def convert_coords(self, x: float, y: float) -> typing.Tuple[float, float]:
        """
        Converts the coordinates relative to the camera
        """
        return x - self.camera.x, y - self.camera.y

    def play_sound(self, sound: pygame.mixer.Sound, loops: int = 0, left: float = 1.0, right: float = 1.0):
        """
        Plays a sound
        :param sound: the Pygame Sound object to play
        :param loops:
        :param left: the left volume to play the sound (0-1)
        :param right: the right volume to play the sound (0-1)

        For example, if left is 0 and right is 1, then the sound will only be played out of the right speaker/earphone
        """
        channel = pygame.mixer.Sound.play(sound, loops=loops)
        channel.set_volume(left, right)

    def get_cursor_pos(self) -> typing.Tuple[float, float]:
        """
        Returns the mouse cursor's position
        The position is automatically scaled so this is the safest way to get the position
        """
        return self.screen_manager.scale_coords(pygame.mouse.get_pos())

    def on_message_receive(self, message: str, sender):
        """
        This event is triggered whenever a message is sent
        :param message:
        :param sender: the object which broadcast the message
        """
        pass

    def broadcast_message(self, message: typing.Union[list, tuple, str], sender=None):
        """
        Broadcasts a message
        :param message:
        :param sender: If not specified, the screen will be flagged as the sender
        Note that the on_message_receive event WILL NOT be triggered for the sender
        """
        if sender is None:
            sender = self

        if self != sender:
            self.on_message_receive(message, sender)

    @abc.abstractmethod
    def handle_input(self, keys: list, mouse: tuple, delta_t: float):
        pass

    @abc.abstractmethod
    def update(self, delta_t: float):
        pass

    @abc.abstractmethod
    def render(self, buffer: pygame.Surface):
        if self.fill_background_color is not None:
            buffer.fill(self.fill_background_color)

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
