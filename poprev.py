import numpy as np
import cv2
from util import get_range_around, highlight_sector
from constants import COLOURS, DRAW_HEIGHT, DRAW_WIDTH, HIGHLIGHT_COLOUR


class PopRev(object):

    def __init__(self):
        self._source_img = None

        self._XSCALE = None
        self._YSCALE = None

        self._export = np.ones((DRAW_HEIGHT, DRAW_WIDTH, 3), dtype=np.uint8) * 255
        self._selections = np.ones((DRAW_HEIGHT, DRAW_WIDTH), dtype=np.uint8) * 9

        self._save_name = None

        self._unsaved_changes = False

    def get_selection(self, x, y):
        return self._selections[y, x]

    def get_ref_sector(self, x, y):
        return self._source_img[int(y * self._YSCALE): int((y + 1) * self._YSCALE),
               int(x * self._XSCALE): int((x + 1) * self._XSCALE)]

    def get_ref_context(self, x, y, width, height, level):
        xl, xu = get_range_around(x, 0, DRAW_WIDTH - 1, level)
        yl, yu = get_range_around(y, 0, DRAW_HEIGHT - 1, level)

        extract = self._source_img[int(yl * self._YSCALE): int((yu + 1) * self._YSCALE),
                  int(xl * self._XSCALE): int((xu + 1) * self._XSCALE)]

        resize = cv2.resize(extract, (width, height),
                            interpolation=cv2.INTER_NEAREST)

        highlight_sector(resize, x - xl, y - yl, 2 * level + 1,
                         2 * level + 1, 1,HIGHLIGHT_COLOUR)

        return resize

    def get_preview(self, x, y):
        preview = np.copy(self._export)
        preview[y, x] = HIGHLIGHT_COLOUR
        return preview

    def edit_drawing(self, x, y, colour):
        self._export[y, x] = COLOURS[colour]
        self._selections[y, x] = colour
        self._unsaved_changes = True

    def export_drawing(self, filename):
        cv2.imwrite(filename, self._export)

    def save_drawing(self):
        self.save_drawing_as(self._save_name)
        self._unsaved_changes = False

    def save_drawing_as(self, filename):
        file = open(filename, "w")
        out = ""
        for row in self._selections:
            for cell in row:
                out = "{}{}".format(out, str(cell))
            out = "{}{}".format(out, "\n")

        file.write(out)
        file.close()
        self._unsaved_changes = False

        self._save_name = filename

    def load_drawing(self, filename):
        file = open(filename, "r")

        for i, line in enumerate(file):
            line = line[:-1]
            for j, cell in enumerate(line):
                colour = int(cell)
                self._selections[i, j] = colour

                if not (0 <= colour <= 3):
                    self._export[i, j] = COLOURS[3]
                else:
                    self._export[i, j] = COLOURS[colour]

        file.close()
        self._save_name = filename
        self._unsaved_changes = False

    def load_reference(self, filename):
        self._source_img = cv2.imread(filename, cv2.IMREAD_COLOR)

        self._XSCALE = self._source_img.shape[1] / DRAW_WIDTH
        self._YSCALE = self._source_img.shape[0] / DRAW_HEIGHT

    def has_reference(self):
        return self._source_img is not None

    def get_save_name(self):
        return self._save_name

    def unsaved_changes(self):
        return self._unsaved_changes
