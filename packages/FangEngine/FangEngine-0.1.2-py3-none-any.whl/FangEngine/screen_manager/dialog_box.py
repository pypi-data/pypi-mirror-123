"""
This module contains the base dialog box class
"""
import abc
import typing
import pygame

import FangEngine.screen_manager.base_screen as base_screen


class DialogBox(base_screen.BaseScreen, abc.ABC):
    """
    This class is the class all dialog boxes must inherit from
    """
    def __init__(self, screen_parent: 'base_screen.BaseScreen', *args, **kwargs):
        """
        :param screen_parent:
        :param args:
        :param kwargs:
        """
        super().__init__("DialogBox", screen_parent.screen_manager, *args, **kwargs)

        self.background_color = (100, 100, 100)
        self.size = self.get_size(screen_parent.screen_manager.screen_w, screen_parent.screen_manager.screen_h)
        self.width, self.height = self.size

        self.screen_parent = screen_parent

        self.buffer = pygame.Surface(self.size)

        self.close_button = pygame.Surface((20, 20))
        self.show_close_button = True

        self.x = 0
        self.y = 0

        self.close_button_x = 0
        self.close_button_y = 0
        self.close_button_w = 20
        self.close_button_h = 20

        self.center_dialog_box()
        self.draw_close_button()

    def draw_close_button(self):
        """
        This method is responsible for creating the close button
        Once the buttoh has been drawn it does not need to be drawn again
        (unless you want the appearance of the button to change)
        """
        self.close_button.fill((255, 0, 0))

        pygame.draw.line(self.close_button, (0, 0, 0), (0, 0), (20, 20), 3)
        pygame.draw.line(self.close_button, (0, 0, 0), (20, 0), (0, 20), 3)

        self.close_button_x = self.buffer.get_width() - self.close_button.get_width()
        self.close_button_y = 0

        self.close_button_w = 20
        self.close_button_h = 20

    def __del__(self):
        try:
            self.screen_parent.dialog_boxes.remove(self)
        except ValueError:
            pass

    def broadcast_message(self, message: typing.Union[list, tuple, str], sender=None):
        """
        Broadcasts a message
        :param message:
        :param sender: default is this dialog box
        """
        if sender is None:
            sender = self

        self.screen_parent.on_message_receive(message, sender)

    def center_dialog_box(self):
        """
        Re-calculates the position to draw the dialog box in order to ensure it is centered
        :return:
        """
        self.x = (self.screen_parent.screen_manager.screen_w / 2) - (self.width / 2)
        self.y = (self.screen_parent.screen_manager.screen_h / 2) - (self.height / 2)

    @abc.abstractmethod
    def get_size(self, screen_w: float, screen_h: float) -> tuple:
        """
        This method must return the width and height of the dialog box
        The screen size will be provided if you wish to make the box a scaled percentage of the screen
        :param screen_w:
        :param screen_h:
        :return: the size to make the dialog box
        """
        pass

    def render(self, buffer: pygame.Surface):
        """
        This method draws the dialog box to the specified buffer
        """
        self.buffer.fill(self.background_color)

        if self.show_close_button:
            self.buffer.blit(self.close_button, (self.close_button_x, self.close_button_y))

        self.dialog_render(self.buffer)

        buffer.blit(self.buffer, (self.x, self.y))

    @abc.abstractmethod
    def dialog_render(self, buffer: pygame.Surface):
        """
        This is the method to override for dialog box rendering
        """

    def close(self):
        """
        Closes this dialog box
        """
        self.__del__()

    def on_mouse_button_down(self, pos, button):
        """
        This event is triggered when the box is clicked
        :param pos:
        :param button:
        :return:
        """
        if self.close_button_x <= pos[0] <= self.close_button_x + self.close_button_w and \
                self.close_button_y <= pos[1] <= self.close_button_y + self.close_button_h:
            self.close()

        super(DialogBox, self).on_mouse_button_down(pos, button)

    def convert_coords(self, x: float, y: float) -> typing.Tuple[float, float]:
        """
        This method converts coordinates so (0, 0) is the top left corner of the dialog box, and not the window
        :param x:
        :param y:
        """
        return x - self.x, y - self.y
