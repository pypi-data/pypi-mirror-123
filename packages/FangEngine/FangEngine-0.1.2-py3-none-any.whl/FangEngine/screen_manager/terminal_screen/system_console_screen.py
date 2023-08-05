"""
This module contains the SystemConsoleScreen
"""
import pygame
import os
import subprocess

import FangEngine.screen_manager.terminal_screen.base_console_screen as base_console_screen

pygame.font.init()


class SystemConsoleScreen(base_console_screen.BaseConsoleScreen):
    """
    The SystemConsoleScreen simulates a terminal (ex. cmd on Windows and Bash on Linux)
    """
    def __init__(self, name: str, manager, font: pygame.font.Font):
        """
        :param name:
        :param manager:
        :param font: The pygame font to render all text as
        """
        super().__init__(name, manager, font)
        self.set_prompt(os.getcwd() + "> ")

    def on_input(self, command: str):
        """
        This event is triggered whenever the user inputs a command
        :param command:
        :return:
        """
        if command == "":
            return

        elif command == "clear":
            self.clear_console()

        elif command.startswith("cd"):
            try:
                path = command[command.index(" ") + 1:]
                os.chdir(path)
            except (FileNotFoundError, OSError, ValueError):
                self.add_text("The path could not be found")

            self.set_prompt(os.getcwd() + "> ")

        else:
            try:
                p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                for line in iter(p.stdout.readline, b''):
                    line = line.decode("utf8")
                    self.add_text(line.rstrip("\n"))

                p.stdout.close()
                p.wait()

            except (FileNotFoundError, OSError):
                self.add_text("Command not found")
