import tkinter as tk
from typing import Callable


class Mover(tk.Frame):
    """
    A GUI component which functions as a directional pad i.e. up, down, left,
    and right buttons.
    """

    def __init__(self, master, move_callback: Callable[[str], None],
                 bg: str = "#ffffff"):
        """
        Initialise this Mover.
        :param master: parent container of this Mover
        :param move_callback: function to call when one of the directional
        buttons is pressed
        :param bg: background colour of this Mover
        """
        super().__init__(master, bg=bg)

        self._move_callback = move_callback

        up_btn = tk.Button(self, text="⬆︎", command=self.clicked_up)
        up_btn.grid(row=0, column=1)

        right_btn = tk.Button(self, text="➡︎︎︎", command=self.clicked_right)
        right_btn.grid(row=1, column=2)

        down_btn = tk.Button(self, text="⬇︎︎︎", command=self.clicked_down)
        down_btn.grid(row=2, column=1)

        left_btn = tk.Button(self, text="⬅︎︎︎", command=self.clicked_left)
        left_btn.grid(row=1, column=0)

    def clicked_up(self) -> None:
        """
        Handle the event when the up button is clicked.
        """
        self._move_callback("up")

    def clicked_right(self) -> None:
        """
        Handle the event when the right button is clicked.
        """
        self._move_callback("right")

    def clicked_down(self) -> None:
        """
        Handle the event when the down button is clicked.
        """
        self._move_callback("down")

    def clicked_left(self) -> None:
        """
        Handle the event when the left button is clicked.
        """
        self._move_callback("left")
