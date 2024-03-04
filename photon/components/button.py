from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class Button(Page):
    """
    Represents a button component in the application.

    Args:
        app (Photon): The parent application object.
        text (str): The text to be displayed on the button.
        x (int): The x-coordinate of the button's position. If not set, the button will be centered on X axis.
        y (int): The y-coordinate of the button's position. If not set, the button will be centered on Y axis.
        variant (Variants): The variant of the button (e.g., PRIMARY, SECONDARY, etc.).
        on_click (callable): The function to be called when the button is clicked.
        auto_render (bool): Determines whether the button should be automatically rendered.
    """

    def __init__(self, app, text=None, x=None, y=None, variant: Variants = Variants.PRIMARY, on_click: callable = None, auto_render=True):
        self.app = app
        self.text = text
        self.x = x
        self.y = y
        self.variant = variant
        self.auto_render = auto_render
        
        self.on_click = on_click
        
        if not auto_render: return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        self.on_render(app.sc)
            
    def on_render(self, sc):
        color = theme.get_colors(self.variant)[1]
        
        x = self.x if self.x else utils.centerX(self.app, len(self.text))
        y = self.y if self.y else utils.centerY(self.app)
        
        sc.addstr(y, x, self.text, curses.color_pair(color))
        
    def on_input(self, key):
        if get_key(key) == "enter":
            if self.on_click: self.on_click()