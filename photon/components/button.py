from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class Button:
    def __init__(self, app, text = None, x = None, y = None, variant: Variants = Variants.DEFAULT, on_click: callable = None, auto_render = True):
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