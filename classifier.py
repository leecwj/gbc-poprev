import tkinter as tk
import numpy as np
from typing import Callable

from constants import REF_CANVAS_HEIGHT, REF_CANVAS_WIDTH
from colour_selector import ColourSelector
from preview import Preview


class Classifier(tk.Frame):
    """
    A GUI component that displays an image and allows users to classify the
    image as one of four colours.
    """

    def __init__(self, master, callback: Callable[[int], None],
                 bg: str = "#ffffff"):
        """
        Initialise this Classifier
        :param master: parent container of this Classifier
        :param callback: function to call when the ColourSelector sub-component
        of this Classifier is clicked
        :param bg: the background colour of this Classifier
        """
        super().__init__(master, bg=bg, padx=5)

        self._callback = callback

        self._preview = Preview(self, REF_CANVAS_WIDTH, REF_CANVAS_HEIGHT)
        self._preview.pack(side=tk.TOP)

        self._selector = ColourSelector(self,
                                        ["#000000", "#555555", "#aaaaaa",
                                         "#ffffff"],
                                        ["#ffffff", "#aaaaaa", "#555555",
                                         "#000000"],
                                        self._callback, bg=bg)
        self._selector.pack(side=tk.TOP)

        self._img = None

    def display_image(self, arr: np.ndarray):
        """
        Display an image on the Preview component of this Classifier.
        :param arr: the image to display
        """
        self._preview.display_image(arr)

    def get_selector(self) -> ColourSelector:
        """
        :return: the ColourSelector component of this Classifier.
        """
        return self._selector

    def display_no_image_warning(self) -> None:
        """
        Display a warning that no reference image is loaded.
        """
        self._preview.delete(tk.ALL)
        self._preview.create_text(REF_CANVAS_WIDTH / 2, REF_CANVAS_HEIGHT / 2,
                                  text="Please load a reference image\n "
                                       "by going to File > Load Reference")
