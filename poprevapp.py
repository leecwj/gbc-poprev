import tkinter as tk
from tkinter import filedialog

from poprev import PopRev
from navigator import Navigator
from classifier import Classifier
from preview import Preview
from util import ask_save_before_doing
from constants import DRAW_WIDTH, DRAW_HEIGHT, REF_CANVAS_WIDTH,\
    REF_CANVAS_HEIGHT, PREVIEW_HEIGHT, PREVIEW_WIDTH, BACKGROUND_COLOUR


class PopRevApp(object):

    def __init__(self, master, bg=BACKGROUND_COLOUR):
        self._master = master
        self._bg = bg

        self._file_menu = None

        self._poprev = PopRev()

        self._x = 0
        self._y = 0

        self._classifier = None
        self._preview = None
        self._navigator = None

        self._setup_menu()
        self._setup_view()
        self.refresh_components()

    def _smart_ask_save_before_doing(self, do_fn, title, message):
        if self._poprev.unsaved_changes():
            ask_save_before_doing(lambda: self._smart_save(), do_fn, title,
                                  message)
        else:
            do_fn()

    def _setup_view(self):
        self._navigator = Navigator(self._master, self.handle_move_callback,
                                    self.handle_jump_callback, bg=self._bg)
        self._navigator.pack(side=tk.TOP)

        frame = tk.Frame(self._master, bg=self._bg)
        frame.pack(side=tk.TOP)

        self._classifier = Classifier(frame,
                                      self.handle_select_callback,
                                      bg=self._bg)
        self._classifier.pack(side=tk.LEFT)

        self._preview = Preview(frame, PREVIEW_WIDTH, PREVIEW_HEIGHT,
                                callback=self._handle_preview_click)
        self._preview.pack(side=tk.LEFT)

        self._master.config(bg=self._bg)
        self._master.title("poprev")
        self._master.protocol("WM_DELETE_WINDOW", self._exit)

    def _exit(self):
        title = "Save Before Exiting?"
        message = "Would you like to save this drawing before exiting?"
        self._smart_ask_save_before_doing(lambda: self._master.destroy(),
                                          title, message)

    def _setup_menu(self):
        menu_bar = tk.Menu(self._master)
        self._master.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)

        reference_menu = tk.Menu(file_menu)
        file_menu.add_cascade(label="Reference", menu=reference_menu)

        drawing_menu = tk.Menu(file_menu)
        file_menu.add_cascade(label="Drawing", menu=drawing_menu)

        reference_menu.add_command(label="Load Reference",
                                   command=self.load_reference)

        drawing_menu.add_command(label="New Drawing",
                                 command=self.try_new_drawing)
        drawing_menu.add_command(label="Load Drawing",
                                 command=self.try_load_drawing)
        drawing_menu.add_command(label="Save Drawing",
                                 command=self._smart_save)
        drawing_menu.add_command(label="Save Drawing As",
                                 command=self.save_drawing_as)
        drawing_menu.add_command(label="Export Drawing",
                                 command=self.export_drawing)

        self._file_menu = file_menu

    def _smart_save(self):
        if self._poprev.get_save_name() is None:
            self.save_drawing_as()
        else:
            self.save_drawing()

    def _handle_preview_click(self, x, y):
        jumpx = int(x * DRAW_WIDTH / PREVIEW_WIDTH)
        jumpy = int(y * DRAW_HEIGHT / PREVIEW_HEIGHT)
        self.jump_to(jumpx, jumpy)

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
        if direction == "up":
            self._y = (self._y - 1) % DRAW_HEIGHT
        elif direction == "right":
            self._x = (self._x + 1) % DRAW_WIDTH
        elif direction == "down":
            self._y = (self._y + 1) % DRAW_HEIGHT
        elif direction == "left":
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
            self._classifier.display_image(image)
        else:
            self._classifier.display_no_image_warning()

    def refresh_selector(self):
        selector = self._classifier.get_selector()
        colour = self._poprev.get_selection(self._x, self._y)

        if not (0 <= colour < 4):
            colour = None

        selector.set_selected(colour)

    def refresh_navigator(self):
        self._navigator.display_position(self._x + 1, self._y + 1)

    def handle_select_callback(self, identifier):
        self._poprev.edit_drawing(self._x, self._y, identifier)
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

    def load_drawing(self):
        filename = filedialog.askopenfilename(title="Select Drawing",
                                              filetypes=(("poprev drawing",
                                                          ".poprev"),)
                                              )
        if filename != "":
            self._poprev.load_drawing(filename)
            self.refresh_components()

    def try_load_drawing(self):
        title = "Save Before Loading?"
        message = "Would you like to save this drawing before loading " \
                  "another?"
        self._smart_ask_save_before_doing(lambda: self.load_drawing(),
                                          title, message)

    def new_drawing(self):
        self._poprev.new_drawing()
        self.refresh_components()

    def try_new_drawing(self):
        title = "Save Before Starting Over?"
        message = "Would you like to save this drawing before starting " \
                  "another?"
        self._smart_ask_save_before_doing(lambda: self.new_drawing(),
                                          title, message)

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


if __name__ == "__main__":
    root = tk.Tk()
    app = PopRevApp(root)
    root.mainloop()
