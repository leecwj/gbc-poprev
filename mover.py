import tkinter as tk


class Mover(tk.Frame):

    def __init__(self, master, move_callback, bg="#ffffff"):
        super().__init__(master, bg=bg)

        self._move_callback = move_callback

        north_btn = tk.Button(self, text="⬆︎", command=self.clicked_north)
        north_btn.grid(row=0, column=1)

        east_btn = tk.Button(self, text="➡︎︎︎", command=self.clicked_east)
        east_btn.grid(row=1, column=2)

        south_btn = tk.Button(self, text="⬇︎︎︎", command=self.clicked_south)
        south_btn.grid(row=2, column=1)

        west_btn = tk.Button(self, text="⬅︎︎︎", command=self.clicked_west)
        west_btn.grid(row=1, column=0)

    def clicked_north(self):
        self._move_callback("north")

    def clicked_east(self):
        self._move_callback("east")

    def clicked_south(self):
        self._move_callback("south")

    def clicked_west(self):
        self._move_callback("west")
