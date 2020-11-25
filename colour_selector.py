import tkinter as tk
from typing import Callable, List, Union

from constants import CSO_WIDTH, CSO_HEIGHT


class ColourSelector(tk.Frame):
    """
    A GUI component which allows the user to select one of several colours.
    """

    def __init__(self, master, colours: List[str], highlights: List[str],
                 callback: Callable[[int], None], bg: str = "#ffffff"):
        """
        Initialise this ColourSelector
        :param master: parent container of this ColourSelector
        :param colours: a list of hex strings representing the colours
        available to choose from
        :param highlights: a list of hex strings such that highlights[i] is
        the highlight colour corresponding to colours[i]
        :param callback: function which will be called to notify that a certain
        colour has been chosen, and which colour it is
        :param bg: background colour of this ColourSelector
        """
        super().__init__(master, bg=bg, pady=5)

        self._options2 = []
        self._selected = None
        self._callback = callback

        for i in range(len(colours)):
            cso = ColourSelectorOption(self, colours[i], highlights[i],
                                       self.handle_click_callback, i)
            cso.pack(side=tk.LEFT)
            self._options2.append(cso)

    def handle_click_callback(self, identifier: int) -> None:
        """
        Handles the event in which the user clicks on one of the options in
        this ColourSelector
        :param identifier: the ID of the colour the user clicked on
        """
        self.set_selected(identifier)
        self._callback(identifier)

    def get_selected(self) -> Union[int, None]:
        """
        :return: the ID of the currently selected colour
        """
        return self._selected

    def set_selected(self, identifier: Union[int, None]) -> None:
        """
        Change the selected colour of this ColourSelector
        :param identifier: the ID of the colour to set as selected
        """
        if self._selected is not None:
            self._options2[self._selected].set_selected(False)

        if identifier is not None:
            self._options2[identifier].set_selected(True)

        self._selected = identifier

    def clear_selected(self) -> None:
        """
        Clear the selected colour of this ColourSelector
        """
        self.set_selected(None)


class ColourSelectorOption(tk.Frame):
    """
    A component of the ColourSelector class, which represents a colour that
    the user may select.
    """

    def __init__(self, master, colour: str, highlight: str,
                 callback: Callable[[int], None], identifier: int):
        """
        Initialise this ColourSelectorOption
        :param master: parent container of this ColourSelectorOption
        :param colour: the colour this option represents
        :param highlight: the colour to highlight this option when it is
        selected
        :param callback: the function to call when this option is clicked
        :param identifier: the ID of this option
        """
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

    def handle_click(self, evt: tk.Event) -> None:
        """
        Handle the event in which this ColourSelectorOption is clicked
        :param evt: event object generated when this object is clicked
        """
        self._callback(self._identifier)

    def toggle_selected(self) -> None:
        """
        Toggle this option as selected / not selected
        """
        self._selected = not self._selected

    def set_selected(self, value: bool) -> None:
        """
        Set whether or not this option is selected
        :param value: boolean indicating whether this option is selected or not
        """
        self._selected = value
        self.update_look()

    def update_look(self) -> None:
        """
        Update the appearance of this ColourSelectorOption to indicate whether
        or not it is selected
        """
        if self._selected:
            self._label.config(text="╳️")
        else:
            self._label.config(text="")
