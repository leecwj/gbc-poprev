import tkinter as tk

from constants import REF_CANVAS_HEIGHT, REF_CANVAS_WIDTH
from colour_selector import ColourSelector
from preview import Preview


class Classifier(tk.Frame):
    """

    """

    def __init__(self, master, callback, bg="#ffffff"):
        super().__init__(master, bg=bg, padx=5)

        self._callback = callback

        self._preview = Preview(self, REF_CANVAS_WIDTH, REF_CANVAS_HEIGHT)
        self._preview.pack(side=tk.TOP)

        self._selector = ColourSelector(self,
                                        ["#000000", "#555555", "#aaaaaa",
                                         "#ffffff"],
                                        ["#ffffff", "#aaaaaa", "#555555",
                                         "#000000"],
                                        self.handle_select_callback, bg=bg)
        self._selector.pack(side=tk.TOP)

        self._img = None

    def display_image(self, arr):
        self._preview.display_image(arr)

    def handle_select_callback(self, identifier):
        self._callback(identifier)

    def get_selector(self):
        return self._selector

    def display_no_image_warning(self):
        self._preview.delete(tk.ALL)
        self._preview.create_text(REF_CANVAS_WIDTH / 2, REF_CANVAS_HEIGHT / 2,
                                  text="Please load a reference image\n "
                                       "by going to File > Load Reference")
