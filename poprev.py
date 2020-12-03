import numpy as np
import cv2
from util import get_range_around, highlight_sector, get_img_extract, \
    get_img_sector
from constants import COLOURS, DRAW_HEIGHT, DRAW_WIDTH, HIGHLIGHT_COLOUR, \
    COLOUR_UNKNOWN


class PopRev(object):
    """
    The model for the Picture of Picture Reverser application.
    """

    def __init__(self):
        """
        Initialise the model
        """
        self._ref = None

        # the drawing as it appears when exported
        self._export = None
        # internal representation of the drawing
        self._selections = None

        # name of file the drawing will be saved to
        self._save_name = None

        self._unsaved_changes = False

        self.new_drawing()

    def get_selection(self, x: int, y: int) -> int:
        """
        :param x: x coordinate to retrieve from
        :param y: y coordinate to retrieve from
        :return: the colour of the drawing at the given (x,y) coordinate.
        """
        return self._selections[y, x]

    def get_ref_sector(self, x: int, y: int) -> np.ndarray:
        """
        :param x: x coordinate to retrieve from
        :param y: y coordinate to retrieve from
        :return: sector (x,y) of the reference image
        """
        return get_img_sector(self._ref, x, y, DRAW_WIDTH, DRAW_HEIGHT)

    def get_ref_context(self, x: int, y: int, width: int, height: int,
                        level: int) -> np.ndarray:
        """
        :param x: x coordinate to retrieve from
        :param y: y coordinate to retrieve from
        :param width: width of image to output
        :param height: height of image to output
        :param level: specifies amount context to show
        :return: a portion of the reference image, including sector (x,y) and
        surrounding area. The output will be (2 * level + 1) sectors high and
        wide.
        """
        xl, xu = get_range_around(x, 0, DRAW_WIDTH - 1, level)
        yl, yu = get_range_around(y, 0, DRAW_HEIGHT - 1, level)

        extract = get_img_extract(self._ref, xl, xu, yl, yu, DRAW_WIDTH,
                                  DRAW_HEIGHT)

        resize = cv2.resize(extract, (width, height),
                            interpolation=cv2.INTER_NEAREST)

        highlight_sector(resize, x - xl, y - yl, 2 * level + 1,
                         2 * level + 1, 1, HIGHLIGHT_COLOUR)

        return resize

    def get_preview(self, x: int, y: int) -> np.ndarray:
        """
        :param x: x coordinate to retrieve from
        :param y: y coordinate to retrieve from
        :return: the entire drawing, but with the pixel at (x,y) highlighted
        """
        preview = np.copy(self._export)
        preview[y, x] = HIGHLIGHT_COLOUR
        return preview

    def edit_drawing(self, x: int, y: int, colour: int) -> None:
        """
        Set the colour of the drawing at position (x,y)
        :param x: x coordinate of pixel to edit
        :param y: y coordinate of pixel to edit
        :param colour: colour to set the pixel to
        """
        self._export[y, x] = COLOURS[colour]
        self._selections[y, x] = colour
        self._unsaved_changes = True

    def export_drawing(self, filename: str) -> None:
        """
        Export the drawing as an image
        :param filename: the file to save the exported image to
        """
        cv2.imwrite(filename, self._export)

    def save_drawing(self) -> None:
        """
        Save changes to the current drawing.
        """
        self.save_drawing_as(self._save_name)
        self._unsaved_changes = False

    def save_drawing_as(self, filename: str) -> None:
        """
        Save the current drawing to the specified file
        :param filename: the file to save the drawing to
        """
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

    def load_drawing(self, filename: str) -> None:
        """
        Load the specified drawing
        :param filename: the drawing to load
        """

        file = open(filename, "r")

        for i, line in enumerate(file):
            line = line[:-1]
            for j, cell in enumerate(line):
                colour = int(cell)
                self._selections[i, j] = colour

                if not (0 <= colour < 4):
                    self._export[i, j] = COLOURS[3]
                else:
                    self._export[i, j] = COLOURS[colour]

        file.close()
        self._save_name = filename
        self._unsaved_changes = False

    def load_reference(self, filename: str) -> None:
        """
        Load the specified reference image
        :param filename: the reference image to load
        """
        self._ref = cv2.imread(filename, cv2.IMREAD_COLOR)

    def has_reference(self) -> bool:
        """
        :return: True if a reference has been loaded.
        """
        return self._ref is not None

    def get_save_name(self) -> str:
        """
        :return: the filename of the current drawing
        """
        return self._save_name

    def unsaved_changes(self) -> bool:
        """
        :return: True if unsaved changes have been made to the current drawing
        """
        return self._unsaved_changes

    def new_drawing(self) -> None:
        """
        Set up model state for a blank drawing.
        """
        self._export = np.ones((DRAW_HEIGHT, DRAW_WIDTH, 3),
                               dtype=np.uint8) * 255
        self._selections = np.ones((DRAW_HEIGHT, DRAW_WIDTH),
                                   dtype=np.uint8) * COLOUR_UNKNOWN
        self._save_name = None
        self._unsaved_changes = False
