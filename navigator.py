import tkinter as tk

from mover import Mover
from jumper import Jumper


class Navigator(tk.Frame):

    def __init__(self, master, move_callback, jump_callback, bg="#ffffff"):
        super().__init__(master, bg=bg)

        self._mover = Mover(self, move_callback, bg=bg)
        self._mover.pack(side=tk.LEFT)

        self._jumper = Jumper(self, jump_callback, bg=bg)
        self._jumper.pack(side=tk.LEFT)

    def display_position(self, x, y):
        self._jumper.display_position(x, y)
