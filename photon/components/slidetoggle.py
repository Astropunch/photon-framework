from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class SlideToggle(Page):
    """
    Represents a slide toggle component.

    Args:
        app (Photon): The application instance.
        x (int): The x-coordinate of the slide toggle's position. If None, it will be centered horizontally.
        y (int): The y-coordinate of the slide toggle's position. If None, it will be centered vertically.
        checked (bool): The initial state of the slide toggle. Default is False.
        enabled (Variants): The variant for the enabled state. Default is Variants.SUCCESS.
        disabled (Variants): The variant for the disabled state. Default is Variants.ERROR.
        char (str): The character to display in the slide toggle. Default is "@".
        auto_render (bool): Whether to automatically render the slide toggle. Default is True.
    """

    def __init__(self, app, x=None, y=None, checked=False, enabled: Variants = Variants.SUCCESS, disabled: Variants = Variants.ERROR,
                 char: str = "@", auto_render=True):
        self.app = app
        self.x = x if x is not None else utils.centerX(app, 4)
        self.y = y if y is not None else utils.centerY(app, 1)
        self.checked = checked
        self.char = char
        self.enabled = enabled
        self.disabled = disabled

        if not auto_render:
            return

        if not app.sc:
            raise Exception("App screen is not initialized.")

        self.on_render(app.sc)

    def on_render(self, sc):
        enabled = theme.get_colors(self.enabled)[1]
        disabled = theme.get_colors(self.disabled)[1]

        box = f"[ {self.char}]" if self.checked else f"[{self.char} ]"
        sc.addstr(self.y, self.x, box, curses.color_pair(enabled if self.checked else disabled))

    def on_input(self, key):
        if get_key(key) in [" ", "enter"]:
            self.checked = not self.checked