from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class Enum(Page):
    """
    Represents a selectable enumeration component.

    Args:
        app (Photon): The parent application.
        values (list, optional): The list of values to be displayed. Defaults to an empty list.
        x (int, optional): The x-coordinate of the component's position. If not set, the enum will be centered on X axis.
        y (int, optional): The y-coordinate of the component's position. If not set, the enum will be centered on Y axis.
        selected (int, optional): The index of the initially selected value. Defaults to 0.
        variant (Variants, optional): The variant of the component. Defaults to Variants.DEFAULT.
        loop (bool, optional): Whether the selection should loop around. Defaults to True.
        reverse (bool, optional): Whether the component color should be rendered in reverse. Defaults to False.
        on_click (callable, optional): The callback function to be called when a value is selected. Defaults to None.
        auto_render (bool, optional): Whether the component should be automatically rendered. Defaults to True.
    """

    def __init__(self, app, values: list = [], x = None, y = None, selected = 0, variant:Variants = Variants.DEFAULT, loop:bool = True,
                 reverse = False, on_click: callable = None, auto_render = True):
        self.app = app
        
        self.values = values if len(values) > 0 else ["Hello", "World"]
        self.x = x
        self.y = y
        
        
        self.index = selected
        self.variant = variant
        self.reverse = reverse
        self.loop = loop
        
        self.selected = None
        
        self.callback = on_click
        
        if not auto_render: return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        self.on_render(app.sc)
        
    def on_render(self, sc):
        primary = theme.get_colors(self.variant)[1 if self.reverse else 0]
        
        if self.index > len(self.values) - 1: self.index = len(self.values) - 1
        if self.index < 0: self.index = 0
        
        self.selected = self.values[self.index]
        text = f"< {self.selected} >"
        
        x = self.x if self.x else utils.centerX(self.app, len(text))
        y = self.y if self.y else utils.centerY(self.app)
        
        sc.addstr(y, x, text, curses.color_pair(primary))
        
    def on_input(self, key):
        match get_key(key):
            case "left":
                self.index -= 1
                if self.loop and self.index < 0:
                    self.index = len(self.values) - 1
                
            case "right":
                self.index += 1
                if self.loop and self.index > len(self.values) - 1:
                    self.index = 0
                
            case "enter":
                if self.callback:
                    self.callback(self.selected, self.index)    