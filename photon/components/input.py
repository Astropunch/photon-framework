from ..page import Page
from ..theme import Variants
from ..core import theme
from .. import utils
from ..keymap import get_key

import curses

class Input(Page):
    """
    Represents an input component that allows the user to enter text.

    Args:
        app (Photon): The parent application object.
        title (str): The title of the input component.
        variant (Variants, optional): The variant of the input component. Defaults to Variants.PRIMARY.
        width (int, optional): The width of the input component. Defaults to 30.
        callback (callable, optional): A callback function to be called when the user presses enter. Defaults to None.
        auto_render (bool, optional): Whether to automatically render the input component. Defaults to True.
    """

    def __init__(self, app, title, variant: Variants = Variants.PRIMARY, width: int = 30,
                 callback: callable = None, auto_render=True):
        self.app = app
        self.title = title if title else "Input"
        self.variant = variant
        self.width = width

        self.value = ""
        self.render_value = ""

        self.callback = callback

        if not auto_render:
            return

        if not app.sc:
            raise Exception("App screen is not initialized.")

        self.on_render(app.sc)

    def on_render(self, sc):
        curses.curs_set(1)

        # normal input
        ##############
        # Hello_____ #
        ##############

        # overflow
        ##############
        # ...o World #
        ##############

        primary_bg = theme.get_colors(self.variant)[1]

        if len(self.value) == 0:
            self.render_value = "_" * (self.width - 4)
        elif len(self.value) > self.width - 4:
            self.render_value = "..." + self.value[-(self.width - 7):]
        else:
            self.render_value = self.value + "_" * (self.width - 4 - len(self.value))

        # get start of the Y axis
        sizeY = 3
        y = utils.centerY(self.app, sizeY)

        # get start of the X axis
        maxX = 0
        for ln in [self.render_value, self.title]:
            maxX = len(ln) if len(ln) > maxX else maxX
        maxX += 4

        if maxX < self.width:
            maxX = self.width

        x = utils.centerX(self.app, maxX)

        # draw the modal

        # draw the background
        for i in range(y, y + sizeY):
            sc.addstr(i, x, " " * maxX, curses.color_pair(primary_bg))

        # draw the border
        sc.addstr(y, x, "#" * maxX, curses.color_pair(primary_bg))  # top
        sc.addstr(y + sizeY - 1, x, "#" * maxX, curses.color_pair(primary_bg))  # bottom
        for i in range(y, y + sizeY):
            sc.addstr(i, x, "#", curses.color_pair(primary_bg))  # left
            sc.addstr(i, x + maxX - 1, "#", curses.color_pair(primary_bg))  # right

        # draw the title
        title = f"] {self.title} ["
        sc.addstr(y, utils.centerTextX(self.app, title), title, curses.color_pair(primary_bg))

        # draw the content
        sc.addstr(y + 1, x + 2, self.render_value, curses.color_pair(primary_bg))

    def on_input(self, key):
        key = get_key(key)

        if key == "backspace":
            self.value = self.value[:-1]
            return

        if key == "enter":
            if self.callback:
                self.callback(self.value)
                curses.curs_set(0)

        if len(key) == 1:
            self.value += key
            return