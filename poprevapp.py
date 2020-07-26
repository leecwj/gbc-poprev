import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog

from poprev import PopRev
from util import ask_save_before_doing
from constants import DRAW_WIDTH, DRAW_HEIGHT, REF_CANVAS_WIDTH,\
    REF_CANVAS_HEIGHT, CSO_WIDTH, CSO_HEIGHT, BACKGROUND_COLOUR


class PopRevApp(object):

    def __init__(self, master, bg=BACKGROUND_COLOUR):
        self._master = master
        self._bg = bg

        self._file_menu = None

        self._poprev = PopRev()

        self._x = 0
        self._y = 0

        self._refexplorer = None
        self._preview = None
        self._navigator = None

        self._setup_menu()
        self._setup_view()
        self.refresh_components()

    def _setup_view(self):
        self._navigator = Navigator(self._master, self.handle_move_callback,
                                    self.handle_jump_callback, bg=self._bg)
        self._navigator.pack(side=tk.TOP)

        frame = tk.Frame(self._master, bg=self._bg)
        frame.pack(side=tk.TOP)

        self._refexplorer = ReferenceExplorer(frame,
                                              self.handle_select_callback,
                                              bg=self._bg)
        self._refexplorer.pack(side=tk.LEFT)

        self._preview = Preview(frame, 4 * DRAW_WIDTH, 4 * DRAW_HEIGHT)
        self._preview.pack(side=tk.LEFT)

        self._master.config(bg=self._bg)
        self._master.title("poprev")
        self._master.protocol("WM_DELETE_WINDOW", self._exit)

    def _exit(self):
        if self._poprev.unsaved_changes():
            ask_save_before_doing(lambda: self._smart_save(),
                                  lambda: self._master.destroy(),
                                  "Save Before Exiting?",
                                  "Do you want to save the current drawing "
                                  "before exiting?")
        else:
            self._master.destroy()

    def _setup_menu(self):
        menu_bar = tk.Menu(self._master)
        self._master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Reference",
                              command=self.load_reference)
        file_menu.add_command(label="Load Drawing",
                              command=self.try_load_drawing)
        file_menu.add_command(label="Save Drawing", command=self.save_drawing)
        file_menu.add_command(label="Save Drawing As",
                              command=self.save_drawing_as)
        file_menu.add_command(label="Export Drawing",
                              command=self.export_drawing)

        file_menu.entryconfig(2, state=tk.DISABLED)

        self._file_menu = file_menu

    def _smart_save(self):
        if self._poprev.get_save_name() is None:
            self.save_drawing_as()
        else:
            self.save_drawing()

    def load_reference(self):
        filename = filedialog.askopenfilename(title="Open Reference Image",
                                              filetypes=(
                                                  ("jpeg files", "*.jpg"),
                                                  ("jpeg files", "*.jpeg"),
                                                  ("png files", "*.png")
                                              )
                                              )
        if filename != "":
            self._poprev.load_reference(filename)
            self.refresh_components()

    def next_pixel(self):
        self._x = (self._x + 1) % DRAW_WIDTH
        if self._x == 0:
            self._y = (self._y + 1) % DRAW_HEIGHT

        self.refresh_components()

    def move_to(self, direction):
        if direction == "north":
            self._y = (self._y - 1) % DRAW_HEIGHT
        elif direction == "east":
            self._x = (self._x + 1) % DRAW_WIDTH
        elif direction == "south":
            self._y = (self._y + 1) % DRAW_HEIGHT
        elif direction == "west":
            self._x = (self._x - 1) % DRAW_WIDTH

        self.refresh_components()

    def jump_to(self, x, y):
        self._x = x
        self._y = y

        self.refresh_components()

    def refresh_components(self):
        self.refresh_selector()
        self.refresh_preview()
        self.refresh_title()
        self.refresh_navigator()

    def refresh_preview(self):
        self._preview.display_image(self._poprev.get_preview(self._x, self._y))

        if self._poprev.has_reference():
            image = self._poprev.get_ref_context(self._x, self._y,
                                                 REF_CANVAS_WIDTH,
                                                 REF_CANVAS_HEIGHT, 1)
            self._refexplorer.display_image(image)
        else:
            self._refexplorer.display_no_image_warning()

    def refresh_selector(self):
        selector = self._refexplorer.get_selector()
        colour = self._poprev.get_selection(self._x, self._y)

        if not (0 <= colour < 4):
            colour = None

        selector.set_selected(colour)

    def refresh_navigator(self):
        self._navigator.display_position(self._x + 1, self._y + 1)

    def handle_select_callback(self, id):
        self._poprev.edit_drawing(self._x, self._y, id)
        self.next_pixel()

    def export_drawing(self):
        filename = filedialog.asksaveasfilename(title="Export Drawing",
                                                filetypes=(("png files",
                                                            "*.png"),)
                                                )
        if filename != "":
            self._poprev.export_drawing(filename)

    def save_drawing(self):
        self._poprev.save_drawing()
        self.refresh_title()

    def save_drawing_as(self):
        filename = filedialog.asksaveasfilename(title="Save Drawing As",
                                                filetypes=(("poprev drawing",
                                                            ".poprev"),))
        if filename != "":
            self._poprev.save_drawing_as(filename)
            self.refresh_title()

            self._file_menu.entryconfig(2, state=tk.ACTIVE)

    def load_drawing(self):
        filename = filedialog.askopenfilename(title="Select Drawing",
                                              filetypes=(("poprev drawing",
                                                          ".poprev"),)
                                              )
        if filename != "":
            self._poprev.load_drawing(filename)
            self.refresh_components()

    def try_load_drawing(self):
        if self._poprev.unsaved_changes():
            ask_save_before_doing(lambda: self._smart_save(),
                                  lambda: self.load_drawing(),
                                  "Save Before Loading?",
                                  "Would you like to save this drawing before "
                                  "loading another?")
        else:
            self.load_drawing()

    def handle_move_callback(self, direction):
        self.move_to(direction)

    def handle_jump_callback(self, x, y):
        self.jump_to(x - 1, y - 1)

    def refresh_title(self):
        unsaved_changes = ""
        if self._poprev.unsaved_changes():
            unsaved_changes = "*"

        name = "untitled"
        if self._poprev.get_save_name() is not None:
            name = self._poprev.get_save_name()

        self._master.title("poprev ({}){}".format(name, unsaved_changes))


class ReferenceExplorer(tk.Frame):

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

    def handle_select_callback(self, id):
        self._callback(id)

    def get_selector(self):
        return self._selector

    def display_no_image_warning(self):
        self._preview.delete("all")
        self._preview.create_text(REF_CANVAS_WIDTH / 2, REF_CANVAS_HEIGHT / 2,
                                  text="Please load a reference image\n "
                                       "by going to File > Load Reference")


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
        self.delete("all")
        self.create_image(0, 0, anchor="nw", image=self._img)


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

    def handle_click_callback(self, id):
        self.set_selected(id)
        self._callback(id)

    def get_selected(self):
        return self._selected

    def set_selected(self, id):
        if not self._selected is None:
            self._options2[self._selected].set_selected(False)

        if not id is None:
            self._options2[id].set_selected(True)

        self._selected = id

    def clear_selected(self):
        self.set_selected(None)


class ColourSelectorOption(tk.Frame):

    def __init__(self, master, colour, highlight, callback, id):
        super().__init__(master, bg=colour, height=CSO_HEIGHT, width=CSO_WIDTH)

        self.callback = callback
        self.id = id

        self.pack_propagate(False)

        self._selected = False

        self._label = tk.Label(self, text="", font=("Arial", 48), bg=colour,
                               width=CSO_WIDTH, justify=tk.CENTER,
                               fg=highlight)
        self._label.pack(side=tk.LEFT)

        self.bind("<Button-1>", self.handle_click)
        self._label.bind("<Button-1>", self.handle_click)

    def handle_click(self, evt):
        self.callback(self.id)

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


class Navigator(tk.Frame):

    def __init__(self, master, move_callback, jump_callback, bg="#ffffff"):
        super().__init__(master, bg=bg)

        self._mover = Mover(self, move_callback, bg=bg)
        self._mover.pack(side=tk.LEFT)

        self._jumper = Jumper(self, jump_callback, bg=bg)
        self._jumper.pack(side=tk.LEFT)

    def display_position(self, x, y):
        self._jumper.display_position(x, y)


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


class Jumper(tk.Frame):

    def __init__(self, master, jump_callback,
                 xl=1, xu=DRAW_WIDTH, yl=1, yu=DRAW_HEIGHT, bg="#ffffff"):
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

    def click_callback(self):
        x = self._xentry.get()
        y = self._yentry.get()

        if not (x.isnumeric() and y.isnumeric()):
            return  # silently fail

        x = int(x)
        y = int(y)

        if not (self._xl <= x <= self._xu and self._yl <= y <= self._yu):
            return  # silently fail

        self._jump_callback(x, y)

    def display_position(self, x, y):
        self._xentry.delete(0, tk.END)
        self._xentry.insert(0, str(x))

        self._yentry.delete(0, tk.END)
        self._yentry.insert(0, str(y))


if __name__ == "__main__":
    root = tk.Tk()
    app = PopRevApp(root)
    root.mainloop()
