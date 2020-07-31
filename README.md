﻿# Game Boy Camera Picture of Picture Reverser (gbcpoprev)

The  **G**ame **B**oy **C**amera **P**icture **o**f **P**icture **Rev**erser is an application aimed at providing an easily accessible way of transferring photos taken on a [Game Boy Camera](https://en.wikipedia.org/wiki/Game_Boy_Camera) to a computer.

## Installing
This app is written in and requires python to run.

In addition, the following python packages are required
- numpy
- opencv-python
- Pillow
- tkinter

e.g.
`pip3 install numpy opencv-python Pillow`

After python and the required packages are installed, clone this repository.
`git clone https://github.com/leecwj/gbc-poprev.git`

Next, navigate to the newly created copy of the repository.
`cd gbc-poprev`

Execute the application via the entry point, `poprevapp.py`, e.g.
`python3 poprevapp.py`

## How to Use
The purpose of this app is recreate GB Camera photographs by using a photograph of the photograph as a reference image, such as the one below.

![A photograph of a Game Boy Advance displaying a photograph taken by a Game Boy Camera.](https://i.imgur.com/dWl7dSZ.jpg)

This app relies on the reference image being deskewed and cropped like so.

![A deskewed and cropped version of the previous image.](https://i.imgur.com/4srNywK.png)

Currently, this cannot be done in the app itself. However, there are plans to implement this feature in the future.

To begin, load a reference image (such as the one above) by going to File > Load Reference.

The reference image will be displayed on the left.

![Screenshot of program.](https://i.imgur.com/an0m3WS.png)
In particular, the editor will zoom in on the top left corner of the reference image, and an area of the image will be outlined in red. This highlighted area is a single pixel of the original photo.

Below the reference image are four buttons. They are used to classify the pixel highlighted in red.

In this example, the highlighted pixel is white. Clicking the white button records this selection and moves to the next pixel.

![Screenshot of program.](https://i.imgur.com/fkAP5ww.png)
As more pixels are classified, a preview of the reconstruction appears on the right.

After many more pixels are classified, the image may look like this, resembling the reference image as intended.
![Screenshot of program.](https://i.imgur.com/VC3YMJR.png)