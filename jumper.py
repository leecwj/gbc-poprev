import tkinter as tk
from typing import Callable

from constants import DRAW_WIDTH, DRAW_HEIGHT


class Jumper(tk.Frame):
    """
    A GUI component that allows the user to specify and "jump" to an
    (x, y) coordinate.
    """

    def __init__(self, master, jump_callback: Callable[[int, int], None],
                 xl: int = 1, xu: int = DRAW_WIDTH, yl: int = 1,
                 yu: int = DRAW_HEIGHT, bg: str = "#ffffff"):
        """
        Initialise this Jumper
        :param master: parent container of this Jumper
        :param jump_callback: function to call when the user clicks the jump
        button
        :param xl: lower bound on the allowed range of x coordinates
        :param xu: upper bound on the allowed range of x coordinates
        :param yl: lower bound on the allowed range of y coordinates
        :param yu: upper bound on the allowed range of y coordinates
        :param bg: background colour of this Jumper
        """
        super().__init__(master, bg=bg)

        self._xl = xl
        self._xu = xu
        self._yl = yl
        self._yu = yu

        self._jump_callback = jump_callback

        label1 = tk.Label(self, text="x:", bg=bg)
        label1.pack(side=tk.LEFT)

        self._xentry = tk.Entry(self, width=3)
        self._xentry.pack(side=tk.LEFT)

        label2 = tk.Label(self, text="y:", bg=bg)
        label2.pack(side=tk.LEFT)

        self._yentry = tk.Entry(self, width=3)
        self._yentry.pack(side=tk.LEFT)

        jump_btn = tk.Button(self, text="Jump", command=self.click_callback)
        jump_btn.pack(side=tk.LEFT)

    def click_callback(self) -> None:
        """
        Handles the event when the jump button is clicked
        """
        x = self._xentry.get()
        y = self._yentry.get()

        if not (x.isnumeric() and y.isnumeric()):
            return  # silently fail

        x = int(x)
        y = int(y)

        if not (self._xl <= x <= self._xu and self._yl <= y <= self._yu):
            return  # silently fail

        self._jump_callback(x, y)

    def display_position(self, x: int, y: int) -> None:
        """
        Display a given (x, y) coordinate in this object's text entry fields.
        :param x: x coordinate to display
        :param y: y coordinate to display
        """
        self._xentry.delete(0, tk.END)
        self._xentry.insert(0, str(x))

        self._yentry.delete(0, tk.END)
        self._yentry.insert(0, str(y))
