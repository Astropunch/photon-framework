from ..page import Page
from ..core import theme
from ..theme import Variants
from .. import utils

import curses

class Modal(Page):
    """
    Represents a modal component that can be rendered on the screen.

    Args:
        app (Photon): The application instance.
        title (str, optional): The title of the modal. Defaults to "Modal".
        content (str, optional): The content of the modal. Defaults to "This is a modal.".
        variant (Variants, optional): The variant of the modal. Defaults to Variants.PRIMARY.
        auto_render (bool, optional): Whether to automatically render the modal. Defaults to True.
    """

    def __init__(self, app, title="", content="", variant: Variants = Variants.PRIMARY, auto_render=True):
        self.app = app
        self.title = title if title else "Modal"
        self.content = content if content else "This is a modal."
        self.variant = variant

        if not auto_render:
            return

        if not app.sc:
            raise Exception("App screen is not initialized.")

        self.on_render(app.sc)

    def on_render(self, sc):
        ###] Modal [################
        # This is a modal.         #
        ############################

        primary_bg = theme.get_colors(self.variant)[1]

        # get start of the Y axis
        sizeY = len(self.content.splitlines()) + 2
        y = utils.centerY(self.app, sizeY)

        # get start of the X axis
        maxX = 0
        for ln in self.content.splitlines() + [self.title]:
            maxX = len(ln) if len(ln) > maxX else maxX
        maxX += 4

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
        for i, ln in enumerate(self.content.splitlines()):
            sc.addstr(y + 1 + i, utils.centerTextX(self.app, ln), ln, curses.color_pair(primary_bg))

    def on_input(self, key):
        return
        
        
        
