"""
This module contans the base screen for a console
"""
import abc
import typing

import pygame

import FangEngine.screen_manager.terminal_screen.base_terminal_screen as base_terminal_screen

pygame.font.init()


class BaseConsoleScreen(base_terminal_screen.BaseTerminalScreen, abc.ABC):
    """
    The BaseConsoleScreen acts as a command prompt for a CLI applicaiton within the engine
    """
    def __init__(self, name: str, manager, font: pygame.font.Font):
        """
        :param name:
        :param manager:
        :param font: The font to render all text as
        """
        self.prompt = ""
        self.commands = []
        self.input_line = []

        super().__init__(name, manager, font)

        self.set_prompt("> ")

    def set_prompt(self, prompt: str):
        """
        Sets the prompt where the user may issue commands
        """
        self.prompt = prompt
        self.add_string(0, self.height - 1, " " * self.width)
        self.add_string(0, self.height - 1, self.prompt)

    @abc.abstractmethod
    def on_input(self, command: str):
        """
        This event is triggered whenever the user issues a command
        """
        pass

    def add_text(self, text: str):
        """
        Adds a message to the command history
        """
        self.commands.insert(0, text)
        self.redraw_text()

    def add_blank_line(self):
        """
        Inserts a blank like into the command history
        """
        self.commands.insert(0, "")
        self.redraw_text()

    def redraw_text(self):
        """
        Redraws the console
        """
        super(BaseConsoleScreen, self).clear_console()
        for line, cmd in enumerate(self.commands):
            try:
                self.add_string(0, self.height - (line + 2), cmd)
            except pygame.error:
                pass

        self.add_string(0, self.height - 1, self.prompt)

    def clear_console(self, color: typing.Tuple[int, int, int] = None):
        """
        Clears the console of all text
        :param color: the new color to use for the background
        """
        super(BaseConsoleScreen, self).clear_console(color)
        self.commands.clear()
        self.add_string(0, self.height - 1, self.prompt)

    def handle_input(self, keys: list, mouse: tuple, delta_t: float):
        pass

    def update(self, delta_t: float):
        pass

    def on_key_down(self, unicode, key, mod):
        """
        This method can be called to simulate a keypress or overridden to add additional functionality
        """
        if key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
            cmd = "".join(self.input_line)
            self.add_text(self.prompt + cmd)
            self.input_line.clear()
            self.on_input(cmd)
            self.add_string(0, self.height - 1, self.prompt)

        elif key == pygame.K_TAB:
            self.input_line += [" "] * 4

        elif key == pygame.K_BACKSPACE:
            try:
                del self.input_line[-1]
                self.add_character(len(self.input_line) + len(self.prompt), self.height - 1, " ")
            except IndexError:
                pass

        elif key >= pygame.K_SPACE:
            try:
                self.add_character(len(self.input_line) + len(self.prompt), self.height - 1, unicode)
                self.input_line.append(unicode)
            except ValueError:
                pass
