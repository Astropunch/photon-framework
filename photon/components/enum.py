from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class Enum:
    def __init__(self, app, values: list = [], x = None, y = None, selected = 0, variant:Variants = Variants.DEFAULT, loop:bool = True,
                 reverse = False, callback: callable = None, auto_render = True):
        self.app = app
        
        self.values = values if len(values) > 0 else ["Hello", "World"]
        self.x = x
        self.y = y
        
        
        self.index = selected
        self.variant = variant
        self.reverse = reverse
        self.loop = loop
        
        self.selected = None
        
        self.callback = callback
        
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
                
    
    def on_finish(self, func: callable):
        self.call_on_finish = func
        
        
        
        