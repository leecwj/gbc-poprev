from tkinter import messagebox


def get_range_around(x, x_lower, x_upper, r):
    """
    Gets the "range" around a given point
    :param x: The point to get a range around
    :param x_lower: The lower bound of the domain x resides in
    :param x_upper: The upper bound of the domain x resides in
    :param r: The radius of the range to return
    :return: A pair (range_lower, range_upper), which describes a range
            within the domain, of radius r, that contains x.
    """
    range_lower = x - r
    range_upper = x + r

    if range_lower < x_lower:
        range_lower = x_lower
        range_upper = x_lower + (2 * r)

    if range_upper > x_upper:
        range_upper = x_upper
        range_lower = x_upper - (2 * r)

    return range_lower, range_upper


def highlight_sector(img, x, y, width, height, r, colour):
    """
    Draw a rectangle to highlight a "sector" of an image, i.e. a cell, if the
    image was to be divided into a grid
    :param img: The image to draw on
    :param x: The x coordinate of the sector to highlight
    :param y: The y coordinate of the sector to highlight
    :param width: How many sectors wide this image should be divided into
    :param height: How many sectors high this image should be divided into
    :param r: The radius of lines used to draw the rectangle. Specifically, a
                radius k line has a width of 2k + 1 pixels.
    :param colour: The colour of the rectangle to draw
    :return: None
    """
    x1 = int(img.shape[1] / width * x)
    x2 = int(img.shape[1] / width * (x+1))
    y1 = int(img.shape[0] / height * y)
    y2 = int(img.shape[0] / height * (y + 1))

    draw_hline(img, x1, x2, y1, r, colour)
    draw_hline(img, x1, x2, y2, r, colour)
    draw_vline(img, x1, y1, y2, r, colour)
    draw_vline(img, x2, y1, y2, r, colour)


def draw_vline(img, x, y1, y2, r, colour):
    """
    Draw a vertical line on an image.
    :param img: The image to draw on
    :param x: The common x coordinate of the first point of the line.
    :param y1: The y coordinate of the first point of the line
    :param y2:  The y coordinate of the second point of the line
    :param r: The "radius" of the line. Specifically, a radius k line has
                a width of 2k + 1 pixels.
    :param colour: The colour of the line to draw
    :return: None
    """
    draw_solid_rect(img, x - r, x + r + 1, y1, y2, colour)


def draw_hline(img, x1, x2, y, r, colour):
    """
    Draw a horizontal line on an image.
    :param img: The image to draw on
    :param x1: The x coordinate of the first point of the line
    :param x2: The x coordinate of the first point of the line
    :param y: The common y coordinate of the line to draw
    :param r: The "radius" of the line. Specifically, a radius k line has
                a width of 2k + 1 pixels.
    :param colour: The colour of the line to draw.
    :return: None
    """
    draw_solid_rect(img, x1, x2, y - r, y + r + 1, colour)


def draw_solid_rect(img, x1, x2, y1, y2, colour):
    """
    Draw a solid rectangle on an image.
    :param img: The image to draw on
    :param x1: The x coordinate of the first point of the rectangle
    :param x2: The x coordinate of the second point of the rectangle
    :param y1:  The y coordinate of the first point of the rectangle
    :param y2: The y coordinate of the second point of the rectangle
    :param colour: The colour of the rectangle to draw
    :return: None
    """
    for i in range(max(0, x1), min(x2, img.shape[1] - 1)):
        for j in range(max(0, y1), min(y2, img.shape[0] - 1)):
            img[j, i] = colour


def get_img_sector(img, x, y, width, height):
    """
    Get sector (x, y) from an image, i.e. divide the image into a
    width x height grid, and get the cell at (x, y)
    :param img: the image to obtain a sector from
    :param x: The x coordinate of the sector to obtain
    :param y: The y coordinate of the sector to obtain
    :param width: How many sectors wide to divide the image into
    :param height: How many sectors high to divide the image into
    :return:
    """
    return get_img_extract(img, x, x, y, y, width, height)


def get_img_extract(img, x1, x2, y1, y2, width, height):
    """
    Get an extract of an image that includes all sectors of an image such that
    x1 <= x <= x2, y1 <= y <= y2.
    :param img: The image to get an extract of
    :param x1: The lower bound of the x coordinates to extract
    :param x2: The upper bound of the x coordinates to extract
    :param y1: The lower bound of the y coordinates to extract
    :param y2: The upper bound of the y coordinates to extract
    :param width: How many sectors wide to divide the image into
    :param height: How many sectors high to divide the image into
    :return: An extract as described above
    """
    xscale = img.shape[1] / width
    yscale = img.shape[0] / height
    return img[int(y1 * yscale): int((y2 + 1) * yscale),
               int(x1 * xscale): int((x2 + 1) * xscale)]


def ask_save_before_doing(save_fn, do_fn, title, message):
    """
    Ask the user if they would like to save before a certain action proceeds.
    :param save_fn: A no argument function that does the saving
    :param do_fn: A no argument function that does the desired action
    :param title: The title of the message box to display
    :param message: The message to display
    :return: None
    """
    confirm = messagebox.askyesnocancel(title=title,
                                        message=message)
    if confirm is None:
        return
    elif confirm:
        save_fn()

    do_fn()
