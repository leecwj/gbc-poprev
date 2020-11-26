import tkinter as tk
from typing import Callable

from mover import Mover
from jumper import Jumper


class Navigator(tk.Frame):
    """
    Composite GUI element composed of a Mover and a Jumper, allowing a user to
    navigate an x-y space.
    """

    def __init__(self, master, move_callback: Callable[[str], None],
                 jump_callback: Callable[[int, int], None],
                 bg: str = "#ffffff"):
        """
        Initialise this Navigator.
        :param master: parent container of this Navigator
        :param move_callback: function to call when the user clicks on of the
        directional buttons
        :param jump_callback: function to call when the user clicks the jump
        button
        :param bg: background colour of this Navigator
        """
        super().__init__(master, bg=bg)

        self._mover = Mover(self, move_callback, bg=bg)
        self._mover.pack(side=tk.LEFT)

        self._jumper = Jumper(self, jump_callback, bg=bg)
        self._jumper.pack(side=tk.LEFT)

    def display_position(self, x: int, y: int) -> None:
        """
        Display a given (x, y) coordinate in this object's text entry fields.
        :param x: x coordinate to display
        :param y: y coordinate to display
        """
        self._jumper.display_position(x, y)
