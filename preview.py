import cv2
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from typing import Callable, Optional


class Preview(tk.Canvas):
    """
    A GUI element which displays an image.
    """

    def __init__(self, master, width: int, height: int,
                 callback: Optional[Callable[[int, int], None]] = None):
        """
        Initialise this Preview
        :param master: parent container of this Preview
        :param width: the width of this Preview
        :param height: the height of this Preview
        :param callback: function to call if this Preview is clicked
        """
        super().__init__(master, width=width, height=height,
                         highlightthickness=0)

        self._width = width
        self._height = height
        self._img = None
        self._callback = callback

        self.bind("<Button-1>", self.handle_click)

    def display_image(self, arr: np.ndarray) -> None:
        """
        Display an image on this Preview.
        :param arr: the image to display
        """
        new_arr = cv2.resize(arr, (self._width, self._height),
                             interpolation=cv2.INTER_NEAREST)
        self._img = ImageTk.PhotoImage(image=Image.fromarray(new_arr))
        self.delete(tk.ALL)
        self.create_image(0, 0, anchor=tk.NW, image=self._img)

    def handle_click(self, evt: tk.Event) -> None:
        """
        Handle the event in which this Preview is clicked
        :param evt: event object generated when this Preview is clicked
        """
        if self._callback is not None:
            self._callback(evt.x, evt.y)
