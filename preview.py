import cv2
import tkinter as tk
from PIL import Image, ImageTk


class Preview(tk.Canvas):

    def __init__(self, master, width, height):
        super().__init__(master, width=width, height=height,
                         highlightthickness=0)

        self._width = width
        self._height = height
        self._img = None

    def display_image(self, arr):
        new_arr = cv2.resize(arr, (self._width, self._height),
                             interpolation=cv2.INTER_NEAREST)
        self._img = ImageTk.PhotoImage(image=Image.fromarray(new_arr))
        self.delete(tk.ALL)
        self.create_image(0, 0, anchor=tk.NW, image=self._img)
