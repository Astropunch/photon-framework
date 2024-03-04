from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class CheckBox(Page):
    """
    Represents a checkbox component.

    Args:
        app (Photon): The parent application object.
        text (str, optional): The text to display next to the checkbox. Defaults to None.
        x (int, optional): The x-coordinate of the checkbox's position. If not set, the checkbox will be centered on X axis.
        y (int, optional): The y-coordinate of the checkbox's position. If not set, the checkbox will be centered on Y axis.
        checked (bool, optional): The initial state of the checkbox. Defaults to False.
        variant (Variants, optional): The variant of the checkbox. Defaults to Variants.DEFAULT.
        reverse (bool, optional): Whether to reverse the checkbox's color. Defaults to False.
        auto_render (bool, optional): Whether to automatically render the checkbox. Defaults to True.
    """

    def __init__(self, app, text=None, x=None, y=None, checked=False, variant: Variants = Variants.DEFAULT, reverse=False, auto_render=True):
        self.app = app 
        
        self.text = text if text else ""
        self.x = x if x != None else utils.centerX(app, len(self.text) + 4)
        self.y = y if y != None else utils.centerY(app, 1)
        
        self.checked = checked
        self.reverse = reverse
        self.variant = variant
        
        if not auto_render: return
        
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        primary = theme.get_colors(self.variant)[1 if self.reverse else 0]
        sc.addstr(self.y, self.x, ("[x] " if self.checked else f"[ ] ") + str(self.text), curses.color_pair(primary))
        
    def on_input(self, key):
        if get_key(key) in [" ", "enter"]:
            self.checked = not self.checked