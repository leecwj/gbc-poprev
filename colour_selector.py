import tkinter as tk

from constants import CSO_WIDTH, CSO_HEIGHT


class ColourSelector(tk.Frame):

    def __init__(self, master, colours, highlights, callback, bg="#ffffff"):
        super().__init__(master, bg=bg, pady=5)

        self._options2 = []
        self._selected = None
        self._callback = callback

        for i in range(len(colours)):
            cso = ColourSelectorOption(self, colours[i], highlights[i],
                                       self.handle_click_callback, i)
            cso.pack(side=tk.LEFT)
            self._options2.append(cso)

    def handle_click_callback(self, identifier):
        self.set_selected(identifier)
        self._callback(identifier)

    def get_selected(self):
        return self._selected

    def set_selected(self, identifier):
        if self._selected is not None:
            self._options2[self._selected].set_selected(False)

        if identifier is not None:
            self._options2[identifier].set_selected(True)

        self._selected = identifier

    def clear_selected(self):
        self.set_selected(None)


class ColourSelectorOption(tk.Frame):

    def __init__(self, master, colour, highlight, callback, identifier):
        super().__init__(master, bg=colour, height=CSO_HEIGHT, width=CSO_WIDTH)

        self._callback = callback
        self._identifier = identifier

        self.pack_propagate(False)

        self._selected = False

        self._label = tk.Label(self, text="", font=("Arial", 48), bg=colour,
                               width=CSO_WIDTH, justify=tk.CENTER,
                               fg=highlight)
        self._label.pack(side=tk.LEFT)

        self.bind("<Button-1>", self.handle_click)
        self._label.bind("<Button-1>", self.handle_click)

    def handle_click(self, evt):
        self._callback(self._identifier)

    def toggle_selected(self):
        self._selected = not self._selected

    def set_selected(self, value):
        self._selected = value
        self.update_look()

    def update_look(self):
        if self._selected:
            self._label.config(text="╳️")
        else:
            self._label.config(text="")
